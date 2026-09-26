from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.master_data import Category, Location, Product, Warehouse
from app.models.operations import Adjustment, Delivery, Receipt, Transfer
from app.models.stock import StockBalance, StockLedger
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummary,
    LowStockProduct,
    OperationStatusCount,
    RecentMovement,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    warehouse_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve key performance metrics computed directly from database."""
    # 1. Total active products
    prod_q = db.query(Product).filter(Product.is_active.is_(True))
    if category_id:
        prod_q = prod_q.filter(Product.category_id == category_id)
    total_products = prod_q.count()

    # 2. Total warehouses
    total_warehouses = db.query(Warehouse).filter(Warehouse.is_active.is_(True)).count()

    # 3. Product stock totals for Low Stock / Out of Stock
    stock_q = (
        db.query(
            Product.id,
            Product.reorder_level,
            func.coalesce(func.sum(StockBalance.quantity), 0.0).label("total_qty"),
        )
        .outerjoin(StockBalance, Product.id == StockBalance.product_id)
        .filter(Product.is_active.is_(True))
    )
    if category_id:
        stock_q = stock_q.filter(Product.category_id == category_id)
    if warehouse_id:
        stock_q = stock_q.join(Location, StockBalance.location_id == Location.id).filter(
            Location.warehouse_id == warehouse_id
        )

    product_stocks = stock_q.group_by(Product.id, Product.reorder_level).all()

    low_stock_count = 0
    out_of_stock_count = 0
    for ps in product_stocks:
        qty = float(ps.total_qty)
        if qty <= 0:
            out_of_stock_count += 1
            low_stock_count += 1
        elif qty <= float(ps.reorder_level):
            low_stock_count += 1

    # 4. Pending receipts (status != DONE and != CANCELED)
    rec_q = db.query(Receipt).filter(Receipt.status.notin_(["DONE", "CANCELED"]))
    if warehouse_id:
        rec_q = rec_q.filter(Receipt.warehouse_id == warehouse_id)
    pending_receipts = rec_q.count()

    # 5. Pending deliveries
    deliv_q = db.query(Delivery).filter(Delivery.status.notin_(["DONE", "CANCELED"]))
    if warehouse_id:
        deliv_q = deliv_q.filter(Delivery.warehouse_id == warehouse_id)
    pending_deliveries = deliv_q.count()

    # 6. Scheduled transfers
    trans_q = db.query(Transfer).filter(Transfer.status.notin_(["DONE", "CANCELED"]))
    if warehouse_id:
        trans_q = trans_q.filter(Transfer.warehouse_id == warehouse_id)
    scheduled_transfers = trans_q.count()

    return DashboardSummary(
        total_products=total_products,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        pending_receipts=pending_receipts,
        pending_deliveries=pending_deliveries,
        scheduled_transfers=scheduled_transfers,
        total_warehouses=total_warehouses,
    )


@router.get("/operations", response_model=List[OperationStatusCount])
def get_dashboard_operations(
    warehouse_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve operational status counts across Receipts, Deliveries, Transfers, and Adjustments."""
    def count_by_status(model, wh_field="warehouse_id"):
        q = db.query(model.status, func.count(model.id))
        if warehouse_id:
            q = q.filter(getattr(model, wh_field) == warehouse_id)
        results = dict(q.group_by(model.status).all())
        return {
            "draft": results.get("DRAFT", 0),
            "waiting": results.get("WAITING", 0),
            "ready": results.get("READY", 0),
            "done": results.get("DONE", 0),
            "canceled": results.get("CANCELED", 0),
        }

    rec_counts = count_by_status(Receipt)
    del_counts = count_by_status(Delivery)
    trf_counts = count_by_status(Transfer)
    adj_counts = count_by_status(Adjustment)

    return [
        OperationStatusCount(operation_type="RECEIPTS", **rec_counts),
        OperationStatusCount(operation_type="DELIVERIES", **del_counts),
        OperationStatusCount(operation_type="TRANSFERS", **trf_counts),
        OperationStatusCount(operation_type="ADJUSTMENTS", **adj_counts),
    ]


@router.get("/low-stock", response_model=List[LowStockProduct])
def get_dashboard_low_stock(
    warehouse_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve list of products below their reorder threshold."""
    stock_q = (
        db.query(
            Product.id,
            Product.name,
            Product.sku,
            Product.reorder_level,
            func.coalesce(func.sum(StockBalance.quantity), 0.0).label("current_stock"),
        )
        .outerjoin(StockBalance, Product.id == StockBalance.product_id)
        .filter(Product.is_active.is_(True))
    )
    if category_id:
        stock_q = stock_q.filter(Product.category_id == category_id)
    if warehouse_id:
        stock_q = stock_q.join(Location, StockBalance.location_id == Location.id).filter(
            Location.warehouse_id == warehouse_id
        )

    results = (
        stock_q.group_by(Product.id, Product.name, Product.sku, Product.reorder_level)
        .having(func.coalesce(func.sum(StockBalance.quantity), 0.0) <= Product.reorder_level)
        .order_by(func.coalesce(func.sum(StockBalance.quantity), 0.0).asc())
        .limit(limit)
        .all()
    )

    out = []
    for r in results:
        p = db.query(Product).filter(Product.id == r.id).first()
        out.append(
            LowStockProduct(
                product_id=r.id,
                product_name=r.name,
                product_sku=r.sku,
                category_name=p.category.name if p and p.category else None,
                current_stock=float(r.current_stock),
                reorder_level=float(r.reorder_level),
                uom_code=p.uom.code if p and p.uom else None,
            )
        )
    return out


@router.get("/recent-movements", response_model=List[RecentMovement])
def get_recent_movements(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve recent stock movements for the dashboard feed."""
    entries = (
        db.query(StockLedger)
        .order_by(StockLedger.created_at.desc(), StockLedger.id.desc())
        .limit(limit)
        .all()
    )
    return [
        RecentMovement(
            id=e.id,
            date=e.created_at.strftime("%Y-%m-%d %H:%M"),
            product_name=e.product.name if e.product else "Unknown",
            product_sku=e.product.sku if e.product else "Unknown",
            warehouse_name=e.warehouse.name if e.warehouse else "Unknown",
            location_name=e.location.name if e.location else "Unknown",
            operation_type=e.operation_type,
            reference_id=e.reference_id,
            quantity_change=e.quantity_change,
            quantity_after=e.quantity_after,
        )
        for e in entries
    ]
