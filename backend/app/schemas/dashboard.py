from typing import List, Optional
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_products: int
    low_stock_count: int
    out_of_stock_count: int
    pending_receipts: int
    pending_deliveries: int
    scheduled_transfers: int
    total_warehouses: int


class OperationStatusCount(BaseModel):
    operation_type: str  # RECEIPTS, DELIVERIES, TRANSFERS, ADJUSTMENTS
    draft: int = 0
    waiting: int = 0
    ready: int = 0
    done: int = 0
    canceled: int = 0


class LowStockProduct(BaseModel):
    product_id: int
    product_name: str
    product_sku: str
    category_name: Optional[str] = None
    current_stock: float
    reorder_level: float
    uom_code: Optional[str] = None


class RecentMovement(BaseModel):
    id: int
    date: str
    product_name: str
    product_sku: str
    warehouse_name: str
    location_name: str
    operation_type: str
    reference_id: str
    quantity_change: float
    quantity_after: float
