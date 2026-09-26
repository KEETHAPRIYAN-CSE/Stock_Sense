import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.master_data import Product, UOM
from app.models.operations import (
    Adjustment,
    AdjustmentItem,
    Delivery,
    DeliveryItem,
    Receipt,
    ReceiptItem,
    Transfer,
    TransferItem,
)
from app.models.user import User
from app.schemas.operations import (
    AdjustmentCreate,
    AdjustmentDetailOut,
    AdjustmentItemOut,
    AdjustmentOut,
    DeliveryCreate,
    DeliveryDetailOut,
    DeliveryItemOut,
    DeliveryOut,
    ReceiptCreate,
    ReceiptDetailOut,
    ReceiptItemOut,
    ReceiptOut,
    TransferCreate,
    TransferDetailOut,
    TransferItemOut,
    TransferOut,
)
from app.services.inventory_service import InventoryService

router = APIRouter(tags=["Operations"])


def gen_doc_num(prefix: str) -> str:
    now = datetime.now(timezone.utc)
    short_uid = uuid.uuid4().hex[:6].upper()
    return f"{prefix}-{now.strftime('%Y%m%d')}-{short_uid}"


# ============================================================================
# RECEIPTS
# ============================================================================
@router.get("/receipts", response_model=List[ReceiptOut])
def list_receipts(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Receipt)
    if status_filter:
        q = q.filter(Receipt.status == status_filter.upper())
    receipts = q.order_by(Receipt.created_at.desc()).all()

    out = []
    for r in receipts:
        total_items = len(r.items)
        total_qty = sum(item.quantity for item in r.items)
        out.append(
            ReceiptOut(
                id=r.id,
                receipt_number=r.receipt_number,
                supplier_id=r.supplier_id,
                supplier_name=r.supplier.name if r.supplier else "Unknown",
                warehouse_id=r.warehouse_id,
                warehouse_name=r.warehouse.name if r.warehouse else "Unknown",
                destination_location_id=r.destination_location_id,
                destination_location_name=r.destination_location.name if r.destination_location else "Unknown",
                status=r.status,
                scheduled_at=r.scheduled_at,
                created_by_name=r.creator.full_name if r.creator else None,
                created_at=r.created_at,
                validated_at=r.validated_at,
                total_items=total_items,
                total_quantity=total_qty,
            )
        )
    return out


@router.post("/receipts", response_model=ReceiptDetailOut, status_code=status.HTTP_201_CREATED)
def create_receipt(
    receipt_in: ReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not receipt_in.items:
        raise HTTPException(status_code=400, detail="Receipt must contain at least one item.")

    doc_num = receipt_in.receipt_number or gen_doc_num("REC")
    receipt = Receipt(
        receipt_number=doc_num,
        supplier_id=receipt_in.supplier_id,
        warehouse_id=receipt_in.warehouse_id,
        destination_location_id=receipt_in.destination_location_id,
        status="DRAFT",
        scheduled_at=receipt_in.scheduled_at,
        created_by=current_user.id,
    )
    db.add(receipt)
    db.flush()

    for it in receipt_in.items:
        rec_item = ReceiptItem(
            receipt_id=receipt.id,
            product_id=it.product_id,
            quantity=it.quantity,
            uom_id=it.uom_id,
        )
        db.add(rec_item)

    db.commit()
    db.refresh(receipt)
    return get_receipt(receipt.id, db, current_user)


@router.get("/receipts/{receipt_id}", response_model=ReceiptDetailOut)
def get_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Receipt not found")

    items = [
        ReceiptItemOut(
            id=it.id,
            product_id=it.product_id,
            product_name=it.product.name,
            product_sku=it.product.sku,
            quantity=it.quantity,
            uom_id=it.uom_id,
            uom_code=it.uom.code,
        )
        for it in r.items
    ]
    return ReceiptDetailOut(
        id=r.id,
        receipt_number=r.receipt_number,
        supplier_id=r.supplier_id,
        supplier_name=r.supplier.name if r.supplier else "Unknown",
        warehouse_id=r.warehouse_id,
        warehouse_name=r.warehouse.name if r.warehouse else "Unknown",
        destination_location_id=r.destination_location_id,
        destination_location_name=r.destination_location.name if r.destination_location else "Unknown",
        status=r.status,
        scheduled_at=r.scheduled_at,
        created_by_name=r.creator.full_name if r.creator else None,
        created_at=r.created_at,
        validated_at=r.validated_at,
        total_items=len(items),
        total_quantity=sum(it.quantity for it in items),
        items=items,
    )


@router.post("/receipts/{receipt_id}/validate", response_model=ReceiptDetailOut)
def validate_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    service.receive_stock(receipt_id, user_id=current_user.id)
    return get_receipt(receipt_id, db, current_user)


@router.post("/receipts/{receipt_id}/cancel", response_model=ReceiptDetailOut)
def cancel_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    r = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Receipt not found")
    if r.status == "DONE":
        raise HTTPException(status_code=400, detail="Cannot cancel a validated receipt.")
    r.status = "CANCELED"
    db.commit()
    return get_receipt(receipt_id, db, current_user)


# ============================================================================
# DELIVERIES
# ============================================================================
@router.get("/deliveries", response_model=List[DeliveryOut])
def list_deliveries(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Delivery)
    if status_filter:
        q = q.filter(Delivery.status == status_filter.upper())
    deliveries = q.order_by(Delivery.created_at.desc()).all()

    out = []
    for d in deliveries:
        total_items = len(d.items)
        total_qty = sum(item.quantity for item in d.items)
        out.append(
            DeliveryOut(
                id=d.id,
                delivery_number=d.delivery_number,
                customer_id=d.customer_id,
                customer_name=d.customer.name if d.customer else "Unknown",
                warehouse_id=d.warehouse_id,
                warehouse_name=d.warehouse.name if d.warehouse else "Unknown",
                source_location_id=d.source_location_id,
                source_location_name=d.source_location.name if d.source_location else "Unknown",
                status=d.status,
                scheduled_at=d.scheduled_at,
                created_by_name=d.creator.full_name if d.creator else None,
                created_at=d.created_at,
                validated_at=d.validated_at,
                total_items=total_items,
                total_quantity=total_qty,
            )
        )
    return out


@router.post("/deliveries", response_model=DeliveryDetailOut, status_code=status.HTTP_201_CREATED)
def create_delivery(
    deliv_in: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not deliv_in.items:
        raise HTTPException(status_code=400, detail="Delivery must contain at least one item.")

    doc_num = deliv_in.delivery_number or gen_doc_num("DEL")
    deliv = Delivery(
        delivery_number=doc_num,
        customer_id=deliv_in.customer_id,
        warehouse_id=deliv_in.warehouse_id,
        source_location_id=deliv_in.source_location_id,
        status="DRAFT",
        scheduled_at=deliv_in.scheduled_at,
        created_by=current_user.id,
    )
    db.add(deliv)
    db.flush()

    for it in deliv_in.items:
        del_item = DeliveryItem(
            delivery_id=deliv.id,
            product_id=it.product_id,
            quantity=it.quantity,
            uom_id=it.uom_id,
        )
        db.add(del_item)

    db.commit()
    db.refresh(deliv)
    return get_delivery(deliv.id, db, current_user)


@router.get("/deliveries/{delivery_id}", response_model=DeliveryDetailOut)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delivery not found")

    items = [
        DeliveryItemOut(
            id=it.id,
            product_id=it.product_id,
            product_name=it.product.name,
            product_sku=it.product.sku,
            quantity=it.quantity,
            uom_id=it.uom_id,
            uom_code=it.uom.code,
            picked_quantity=it.picked_quantity,
            packed_quantity=it.packed_quantity,
        )
        for it in d.items
    ]
    return DeliveryDetailOut(
        id=d.id,
        delivery_number=d.delivery_number,
        customer_id=d.customer_id,
        customer_name=d.customer.name if d.customer else "Unknown",
        warehouse_id=d.warehouse_id,
        warehouse_name=d.warehouse.name if d.warehouse else "Unknown",
        source_location_id=d.source_location_id,
        source_location_name=d.source_location.name if d.source_location else "Unknown",
        status=d.status,
        scheduled_at=d.scheduled_at,
        created_by_name=d.creator.full_name if d.creator else None,
        created_at=d.created_at,
        validated_at=d.validated_at,
        total_items=len(items),
        total_quantity=sum(it.quantity for it in items),
        items=items,
    )


@router.post("/deliveries/{delivery_id}/pick", response_model=DeliveryDetailOut)
def pick_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if d.status in ["DONE", "CANCELED"]:
        raise HTTPException(status_code=400, detail="Cannot pick in current state.")
    for item in d.items:
        item.picked_quantity = item.quantity
    d.status = "WAITING"
    db.commit()
    return get_delivery(delivery_id, db, current_user)


@router.post("/deliveries/{delivery_id}/pack", response_model=DeliveryDetailOut)
def pack_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if d.status in ["DONE", "CANCELED"]:
        raise HTTPException(status_code=400, detail="Cannot pack in current state.")
    for item in d.items:
        item.packed_quantity = item.picked_quantity
    d.status = "READY"
    db.commit()
    return get_delivery(delivery_id, db, current_user)


@router.post("/deliveries/{delivery_id}/validate", response_model=DeliveryDetailOut)
def validate_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    service.deliver_stock(delivery_id, user_id=current_user.id)
    return get_delivery(delivery_id, db, current_user)


@router.post("/deliveries/{delivery_id}/cancel", response_model=DeliveryDetailOut)
def cancel_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    d = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if d.status == "DONE":
        raise HTTPException(status_code=400, detail="Cannot cancel a validated delivery.")
    d.status = "CANCELED"
    db.commit()
    return get_delivery(delivery_id, db, current_user)


# ============================================================================
# TRANSFERS
# ============================================================================
@router.get("/transfers", response_model=List[TransferOut])
def list_transfers(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Transfer)
    if status_filter:
        q = q.filter(Transfer.status == status_filter.upper())
    transfers = q.order_by(Transfer.created_at.desc()).all()

    out = []
    for t in transfers:
        total_items = len(t.items)
        total_qty = sum(item.quantity for item in t.items)
        out.append(
            TransferOut(
                id=t.id,
                transfer_number=t.transfer_number,
                warehouse_id=t.warehouse_id,
                warehouse_name=t.warehouse.name if t.warehouse else "Unknown",
                source_location_id=t.source_location_id,
                source_location_name=t.source_location.name if t.source_location else "Unknown",
                destination_location_id=t.destination_location_id,
                destination_location_name=t.destination_location.name if t.destination_location else "Unknown",
                status=t.status,
                scheduled_at=t.scheduled_at,
                created_by_name=t.creator.full_name if t.creator else None,
                created_at=t.created_at,
                validated_at=t.validated_at,
                total_items=total_items,
                total_quantity=total_qty,
            )
        )
    return out


@router.post("/transfers", response_model=TransferDetailOut, status_code=status.HTTP_201_CREATED)
def create_transfer(
    trans_in: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not trans_in.items:
        raise HTTPException(status_code=400, detail="Transfer must contain at least one item.")
    if trans_in.source_location_id == trans_in.destination_location_id:
        raise HTTPException(status_code=400, detail="Source and destination locations cannot be identical.")

    doc_num = trans_in.transfer_number or gen_doc_num("TRF")
    transfer = Transfer(
        transfer_number=doc_num,
        warehouse_id=trans_in.warehouse_id,
        source_location_id=trans_in.source_location_id,
        destination_location_id=trans_in.destination_location_id,
        status="READY",
        scheduled_at=trans_in.scheduled_at,
        created_by=current_user.id,
    )
    db.add(transfer)
    db.flush()

    for it in trans_in.items:
        tr_item = TransferItem(
            transfer_id=transfer.id,
            product_id=it.product_id,
            quantity=it.quantity,
            uom_id=it.uom_id,
        )
        db.add(tr_item)

    db.commit()
    db.refresh(transfer)
    return get_transfer(transfer.id, db, current_user)


@router.get("/transfers/{transfer_id}", response_model=TransferDetailOut)
def get_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")

    items = [
        TransferItemOut(
            id=it.id,
            product_id=it.product_id,
            product_name=it.product.name,
            product_sku=it.product.sku,
            quantity=it.quantity,
            uom_id=it.uom_id,
            uom_code=it.uom.code,
        )
        for it in t.items
    ]
    return TransferDetailOut(
        id=t.id,
        transfer_number=t.transfer_number,
        warehouse_id=t.warehouse_id,
        warehouse_name=t.warehouse.name if t.warehouse else "Unknown",
        source_location_id=t.source_location_id,
        source_location_name=t.source_location.name if t.source_location else "Unknown",
        destination_location_id=t.destination_location_id,
        destination_location_name=t.destination_location.name if t.destination_location else "Unknown",
        status=t.status,
        scheduled_at=t.scheduled_at,
        created_by_name=t.creator.full_name if t.creator else None,
        created_at=t.created_at,
        validated_at=t.validated_at,
        total_items=len(items),
        total_quantity=sum(it.quantity for it in items),
        items=items,
    )


@router.post("/transfers/{transfer_id}/validate", response_model=TransferDetailOut)
def validate_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    service.transfer_stock(transfer_id, user_id=current_user.id)
    return get_transfer(transfer_id, db, current_user)


@router.post("/transfers/{transfer_id}/cancel", response_model=TransferDetailOut)
def cancel_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    t = db.query(Transfer).filter(Transfer.id == transfer_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transfer not found")
    if t.status == "DONE":
        raise HTTPException(status_code=400, detail="Cannot cancel a validated transfer.")
    t.status = "CANCELED"
    db.commit()
    return get_transfer(transfer_id, db, current_user)


# ============================================================================
# ADJUSTMENTS
# ============================================================================
@router.get("/adjustments", response_model=List[AdjustmentOut])
def list_adjustments(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Adjustment)
    if status_filter:
        q = q.filter(Adjustment.status == status_filter.upper())
    adjustments = q.order_by(Adjustment.created_at.desc()).all()

    return [
        AdjustmentOut(
            id=a.id,
            adjustment_number=a.adjustment_number,
            warehouse_id=a.warehouse_id,
            warehouse_name=a.warehouse.name if a.warehouse else "Unknown",
            location_id=a.location_id,
            location_name=a.location.name if a.location else "Unknown",
            status=a.status,
            reason=a.reason,
            created_by_name=a.creator.full_name if a.creator else None,
            created_at=a.created_at,
            validated_at=a.validated_at,
            total_items=len(a.items),
        )
        for a in adjustments
    ]


@router.post("/adjustments", response_model=AdjustmentDetailOut, status_code=status.HTTP_201_CREATED)
def create_adjustment(
    adj_in: AdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not adj_in.items:
        raise HTTPException(status_code=400, detail="Adjustment must contain at least one item.")

    doc_num = adj_in.adjustment_number or gen_doc_num("ADJ")
    adj = Adjustment(
        adjustment_number=doc_num,
        warehouse_id=adj_in.warehouse_id,
        location_id=adj_in.location_id,
        reason=adj_in.reason,
        status="DRAFT",
        created_by=current_user.id,
    )
    db.add(adj)
    db.flush()

    service = InventoryService(db)
    for it in adj_in.items:
        bal = service._get_or_create_balance_locked(it.product_id, adj_in.location_id)
        diff = it.counted_quantity - bal.quantity
        adj_item = AdjustmentItem(
            adjustment_id=adj.id,
            product_id=it.product_id,
            system_quantity=bal.quantity,
            counted_quantity=it.counted_quantity,
            difference=diff,
        )
        db.add(adj_item)

    db.commit()
    db.refresh(adj)
    return get_adjustment(adj.id, db, current_user)


@router.get("/adjustments/{adjustment_id}", response_model=AdjustmentDetailOut)
def get_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = db.query(Adjustment).filter(Adjustment.id == adjustment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Adjustment not found")

    items = [
        AdjustmentItemOut(
            id=it.id,
            product_id=it.product_id,
            product_name=it.product.name,
            product_sku=it.product.sku,
            system_quantity=it.system_quantity,
            counted_quantity=it.counted_quantity,
            difference=it.difference,
        )
        for it in a.items
    ]
    return AdjustmentDetailOut(
        id=a.id,
        adjustment_number=a.adjustment_number,
        warehouse_id=a.warehouse_id,
        warehouse_name=a.warehouse.name if a.warehouse else "Unknown",
        location_id=a.location_id,
        location_name=a.location.name if a.location else "Unknown",
        status=a.status,
        reason=a.reason,
        created_by_name=a.creator.full_name if a.creator else None,
        created_at=a.created_at,
        validated_at=a.validated_at,
        total_items=len(items),
        items=items,
    )


@router.post("/adjustments/{adjustment_id}/validate", response_model=AdjustmentDetailOut)
def validate_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = InventoryService(db)
    service.adjust_stock(adjustment_id, user_id=current_user.id)
    return get_adjustment(adjustment_id, db, current_user)


@router.post("/adjustments/{adjustment_id}/cancel", response_model=AdjustmentDetailOut)
def cancel_adjustment(
    adjustment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    a = db.query(Adjustment).filter(Adjustment.id == adjustment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    if a.status == "DONE":
        raise HTTPException(status_code=400, detail="Cannot cancel a validated adjustment.")
    a.status = "CANCELED"
    db.commit()
    return get_adjustment(adjustment_id, db, current_user)
