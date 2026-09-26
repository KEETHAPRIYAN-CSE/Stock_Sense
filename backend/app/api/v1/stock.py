from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.master_data import Product
from app.models.stock import StockBalance
from app.models.user import User
from app.schemas.operations import StockBalanceOut, StockLedgerOut, StockSummaryOut
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/stock", tags=["Stock & Ledger"])


@router.get("", response_model=List[StockSummaryOut])
def get_stock_summary(
    search: Optional[str] = Query(None, description="Search by product name or SKU"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve aggregated stock balances across all locations."""
    service = InventoryService(db)
    items = service.get_stock(search=search)
    out = []
    for item in items:
        p = db.query(Product).filter(Product.id == item["product_id"]).first()
        out.append(
            StockSummaryOut(
                product_id=item["product_id"],
                product_name=item["product_name"],
                product_sku=item["product_sku"],
                category_name=p.category.name if p and p.category else None,
                uom_code=p.uom.code if p and p.uom else None,
                total_quantity=item["total_quantity"],
                reorder_level=item["reorder_level"],
                is_low_stock=item["is_low_stock"],
            )
        )
    return out


@router.get("/ledger", response_model=List[StockLedgerOut])
def get_stock_ledger(
    product_id: Optional[int] = Query(None),
    warehouse_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    operation_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve immutable stock movement ledger entries with filters."""
    service = InventoryService(db)
    entries, _ = service.get_ledger(
        product_id=product_id,
        warehouse_id=warehouse_id,
        location_id=location_id,
        operation_type=operation_type,
        limit=limit,
        offset=offset,
    )
    return [
        StockLedgerOut(
            id=e.id,
            product_id=e.product_id,
            product_name=e.product.name if e.product else "Unknown",
            product_sku=e.product.sku if e.product else "Unknown",
            warehouse_name=e.warehouse.name if e.warehouse else "Unknown",
            location_name=e.location.name if e.location else "Unknown",
            operation_type=e.operation_type,
            reference_type=e.reference_type,
            reference_id=e.reference_id,
            quantity_before=e.quantity_before,
            quantity_change=e.quantity_change,
            quantity_after=e.quantity_after,
            created_by_name=e.user.full_name if e.user else None,
            created_at=e.created_at,
            notes=e.notes,
        )
        for e in entries
    ]


@router.get("/{product_id}", response_model=StockSummaryOut)
def get_product_stock(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve stock balance for a single product."""
    service = InventoryService(db)
    items = service.get_stock()
    match = next((i for i in items if i["product_id"] == product_id), None)
    if not match:
        p = db.query(Product).filter(Product.id == product_id).first()
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")
        return StockSummaryOut(
            product_id=p.id,
            product_name=p.name,
            product_sku=p.sku,
            category_name=p.category.name if p.category else None,
            uom_code=p.uom.code if p.uom else None,
            total_quantity=0.0,
            reorder_level=p.reorder_level,
            is_low_stock=True if p.reorder_level > 0 else False,
        )

    p = db.query(Product).filter(Product.id == product_id).first()
    return StockSummaryOut(
        product_id=match["product_id"],
        product_name=match["product_name"],
        product_sku=match["product_sku"],
        category_name=p.category.name if p and p.category else None,
        uom_code=p.uom.code if p and p.uom else None,
        total_quantity=match["total_quantity"],
        reorder_level=match["reorder_level"],
        is_low_stock=match["is_low_stock"],
    )


@router.get("/{product_id}/locations", response_model=List[StockBalanceOut])
def get_product_stock_by_locations(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve location breakdown for a product."""
    balances = (
        db.query(StockBalance)
        .filter(StockBalance.product_id == product_id, StockBalance.quantity > 0)
        .all()
    )
    return [
        StockBalanceOut(
            id=b.id,
            product_id=b.product_id,
            product_name=b.product.name,
            product_sku=b.product.sku,
            location_id=b.location_id,
            location_name=b.location.name,
            warehouse_name=b.location.warehouse.name,
            quantity=b.quantity,
            uom_code=b.product.uom.code if b.product.uom else None,
            updated_at=b.updated_at,
        )
        for b in balances
    ]
