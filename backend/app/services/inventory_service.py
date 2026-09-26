from datetime import datetime, timezone
from typing import List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.master_data import Location, Product, Warehouse
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
from app.models.stock import StockBalance, StockLedger


def utcnow():
    return datetime.now(timezone.utc)


class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------------
    # Balance Locking Helper
    # ------------------------------------------------------------------------
    def _get_or_create_balance_locked(
        self, product_id: int, location_id: int
    ) -> StockBalance:
        """
        Retrieves or initializes a StockBalance row with row-level locking.
        """
        query = self.db.query(StockBalance).filter(
            StockBalance.product_id == product_id,
            StockBalance.location_id == location_id,
        )
        # Apply row-level lock if supported by the DB dialect
        if self.db.bind and self.db.bind.dialect.name == "postgresql":
            query = query.with_for_update()

        balance = query.first()
        if not balance:
            balance = StockBalance(
                product_id=product_id,
                location_id=location_id,
                quantity=0.0,
            )
            self.db.add(balance)
            self.db.flush()
            self.db.refresh(balance)
        return balance

    # ------------------------------------------------------------------------
    # 1. RECEIVE STOCK
    # ------------------------------------------------------------------------
    def receive_stock(self, receipt_id: int, user_id: Optional[int] = None) -> Receipt:
        """
        Validates an incoming receipt:
        - Locks relevant destination stock balance
        - Increases stock balance: new_stock = old_stock + quantity
        - Inserts append-only StockLedger entry: operation_type = RECEIPT
        - Marks receipt status = DONE
        - Executes atomically
        """
        receipt = self.db.query(Receipt).filter(Receipt.id == receipt_id).first()
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found."
            )

        if receipt.status == "DONE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receipt has already been validated and completed.",
            )
        if receipt.status == "CANCELED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a canceled receipt.",
            )
        if not receipt.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a receipt with no line items.",
            )

        destination_location_id = receipt.destination_location_id
        warehouse_id = receipt.warehouse_id

        for item in receipt.items:
            balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=destination_location_id
            )
            qty_before = balance.quantity
            qty_change = item.quantity
            qty_after = qty_before + qty_change

            # Update stock balance
            balance.quantity = qty_after

            # Create ledger entry
            ledger = StockLedger(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                location_id=destination_location_id,
                operation_type="RECEIPT",
                reference_type="RECEIPT",
                reference_id=receipt.receipt_number,
                quantity_before=qty_before,
                quantity_change=qty_change,
                quantity_after=qty_after,
                created_by=user_id,
                notes=f"Receipt {receipt.receipt_number} from supplier",
            )
            self.db.add(ledger)

        receipt.status = "DONE"
        receipt.validated_by = user_id
        receipt.validated_at = utcnow()
        receipt.updated_at = utcnow()

        self.db.commit()
        self.db.refresh(receipt)
        return receipt

    # ------------------------------------------------------------------------
    # 2. DELIVER STOCK
    # ------------------------------------------------------------------------
    def deliver_stock(self, delivery_id: int, user_id: Optional[int] = None) -> Delivery:
        """
        Validates an outbound delivery:
        - Locks source stock balance
        - Verifies available stock >= delivered quantity (prevents negative stock)
        - Decreases stock balance: new_stock = old_stock - quantity
        - Inserts append-only StockLedger entry: operation_type = DELIVERY
        - Marks delivery status = DONE
        - Executes atomically
        """
        delivery = self.db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if not delivery:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found."
            )

        if delivery.status == "DONE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery has already been validated and completed.",
            )
        if delivery.status == "CANCELED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a canceled delivery.",
            )
        if not delivery.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a delivery with no line items.",
            )

        source_location_id = delivery.source_location_id
        warehouse_id = delivery.warehouse_id

        # Verification step
        for item in delivery.items:
            balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=source_location_id
            )
            if balance.quantity < item.quantity:
                product_name = balance.product.name if balance.product else f"Product #{item.product_id}"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{product_name}'. Available: {balance.quantity}, Requested: {item.quantity}.",
                )

        # Execution step
        for item in delivery.items:
            balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=source_location_id
            )
            qty_before = balance.quantity
            qty_change = -item.quantity
            qty_after = qty_before + qty_change

            balance.quantity = qty_after

            ledger = StockLedger(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                location_id=source_location_id,
                operation_type="DELIVERY",
                reference_type="DELIVERY",
                reference_id=delivery.delivery_number,
                quantity_before=qty_before,
                quantity_change=qty_change,
                quantity_after=qty_after,
                created_by=user_id,
                notes=f"Delivery {delivery.delivery_number} to customer",
            )
            self.db.add(ledger)

        delivery.status = "DONE"
        delivery.validated_by = user_id
        delivery.validated_at = utcnow()
        delivery.updated_at = utcnow()

        self.db.commit()
        self.db.refresh(delivery)
        return delivery

    # ------------------------------------------------------------------------
    # 3. INTERNAL TRANSFER
    # ------------------------------------------------------------------------
    def transfer_stock(self, transfer_id: int, user_id: Optional[int] = None) -> Transfer:
        """
        Validates internal inventory transfer:
        - Locks source and destination balances in strict order (avoids deadlocks)
        - Verifies source stock >= transfer quantity
        - Decreases source location
        - Increases destination location
        - Inserts TRANSFER_OUT ledger row
        - Inserts TRANSFER_IN ledger row
        - Total company inventory remains unchanged
        - Marks transfer status = DONE
        """
        transfer = self.db.query(Transfer).filter(Transfer.id == transfer_id).first()
        if not transfer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found."
            )

        if transfer.status == "DONE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transfer has already been validated.",
            )
        if transfer.status == "CANCELED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a canceled transfer.",
            )
        if transfer.source_location_id == transfer.destination_location_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and destination locations cannot be identical.",
            )
        if not transfer.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a transfer with no items.",
            )

        src_loc_id = transfer.source_location_id
        dst_loc_id = transfer.destination_location_id
        warehouse_id = transfer.warehouse_id

        # Verify source stock
        for item in transfer.items:
            src_balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=src_loc_id
            )
            if src_balance.quantity < item.quantity:
                product_name = src_balance.product.name if src_balance.product else f"Product #{item.product_id}"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient source stock for '{product_name}'. Available: {src_balance.quantity}, Transfer: {item.quantity}.",
                )

        # Execute transfer atomically
        for item in transfer.items:
            src_balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=src_loc_id
            )
            dst_balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=dst_loc_id
            )

            # 1. Source decrease
            src_before = src_balance.quantity
            src_change = -item.quantity
            src_after = src_before + src_change
            src_balance.quantity = src_after

            src_ledger = StockLedger(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                location_id=src_loc_id,
                operation_type="TRANSFER_OUT",
                reference_type="TRANSFER",
                reference_id=transfer.transfer_number,
                quantity_before=src_before,
                quantity_change=src_change,
                quantity_after=src_after,
                created_by=user_id,
                notes=f"Transfer {transfer.transfer_number} to Location #{dst_loc_id}",
            )
            self.db.add(src_ledger)

            # 2. Destination increase
            dst_before = dst_balance.quantity
            dst_change = item.quantity
            dst_after = dst_before + dst_change
            dst_balance.quantity = dst_after

            dst_ledger = StockLedger(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                location_id=dst_loc_id,
                operation_type="TRANSFER_IN",
                reference_type="TRANSFER",
                reference_id=transfer.transfer_number,
                quantity_before=dst_before,
                quantity_change=dst_change,
                quantity_after=dst_after,
                created_by=user_id,
                notes=f"Transfer {transfer.transfer_number} from Location #{src_loc_id}",
            )
            self.db.add(dst_ledger)

        transfer.status = "DONE"
        transfer.validated_by = user_id
        transfer.validated_at = utcnow()
        transfer.updated_at = utcnow()

        self.db.commit()
        self.db.refresh(transfer)
        return transfer

    # ------------------------------------------------------------------------
    # 4. ADJUST STOCK
    # ------------------------------------------------------------------------
    def adjust_stock(self, adjustment_id: int, user_id: Optional[int] = None) -> Adjustment:
        """
        Validates inventory physical count adjustment:
        - Locks stock balance at specified location
        - difference = counted_quantity - system_quantity
        - Sets new stock balance = counted_quantity
        - Inserts ADJUSTMENT ledger row: quantity_change = difference
        - Marks adjustment status = DONE
        """
        adj = self.db.query(Adjustment).filter(Adjustment.id == adjustment_id).first()
        if not adj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Adjustment not found."
            )

        if adj.status == "DONE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Adjustment has already been validated.",
            )
        if adj.status == "CANCELED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate a canceled adjustment.",
            )
        if not adj.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot validate an adjustment with no items.",
            )

        loc_id = adj.location_id
        warehouse_id = adj.warehouse_id

        for item in adj.items:
            balance = self._get_or_create_balance_locked(
                product_id=item.product_id, location_id=loc_id
            )
            system_qty = balance.quantity
            counted_qty = item.counted_quantity
            diff = counted_qty - system_qty

            # Update item record with verified system snapshot
            item.system_quantity = system_qty
            item.difference = diff

            # Update balance
            balance.quantity = counted_qty

            ledger = StockLedger(
                product_id=item.product_id,
                warehouse_id=warehouse_id,
                location_id=loc_id,
                operation_type="ADJUSTMENT",
                reference_type="ADJUSTMENT",
                reference_id=adj.adjustment_number,
                quantity_before=system_qty,
                quantity_change=diff,
                quantity_after=counted_qty,
                created_by=user_id,
                notes=f"Physical count reconciliation ({adj.reason or 'No reason provided'})",
            )
            self.db.add(ledger)

        adj.status = "DONE"
        adj.validated_by = user_id
        adj.validated_at = utcnow()
        adj.updated_at = utcnow()

        self.db.commit()
        self.db.refresh(adj)
        return adj

    # ------------------------------------------------------------------------
    # Stock Queries & Ledger
    # ------------------------------------------------------------------------
    def get_stock(self, search: Optional[str] = None) -> List[dict]:
        """Returns aggregated stock balances across all locations."""
        q = (
            self.db.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.sku.label("product_sku"),
                Product.reorder_level.label("reorder_level"),
                func.coalesce(func.sum(StockBalance.quantity), 0.0).label("total_quantity"),
            )
            .outerjoin(StockBalance, Product.id == StockBalance.product_id)
            .group_by(Product.id, Product.name, Product.sku, Product.reorder_level)
        )
        if search:
            pat = f"%{search.strip()}%"
            q = q.filter((Product.name.ilike(pat)) | (Product.sku.ilike(pat)))

        results = q.order_by(Product.name).all()
        return [
            {
                "product_id": r.product_id,
                "product_name": r.product_name,
                "product_sku": r.product_sku,
                "total_quantity": float(r.total_quantity),
                "reorder_level": float(r.reorder_level),
                "is_low_stock": float(r.total_quantity) <= float(r.reorder_level),
            }
            for r in results
        ]

    def get_stock_by_location(
        self, product_id: Optional[int] = None, location_id: Optional[int] = None
    ) -> List[StockBalance]:
        q = self.db.query(StockBalance).filter(StockBalance.quantity > 0)
        if product_id:
            q = q.filter(StockBalance.product_id == product_id)
        if location_id:
            q = q.filter(StockBalance.location_id == location_id)
        return q.all()

    def get_ledger(
        self,
        product_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        location_id: Optional[int] = None,
        operation_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[StockLedger], int]:
        q = self.db.query(StockLedger)
        if product_id:
            q = q.filter(StockLedger.product_id == product_id)
        if warehouse_id:
            q = q.filter(StockLedger.warehouse_id == warehouse_id)
        if location_id:
            q = q.filter(StockLedger.location_id == location_id)
        if operation_type:
            q = q.filter(StockLedger.operation_type == operation_type)

        total = q.count()
        entries = q.order_by(StockLedger.created_at.desc(), StockLedger.id.desc()).offset(offset).limit(limit).all()
        return entries, total
