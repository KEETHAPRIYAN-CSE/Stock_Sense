from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# STOCK & LEDGER SCHEMAS
# ============================================================================
class StockBalanceOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    location_id: int
    location_name: str
    warehouse_name: str
    quantity: float
    uom_code: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockSummaryOut(BaseModel):
    product_id: int
    product_name: str
    product_sku: str
    category_name: Optional[str] = None
    uom_code: Optional[str] = None
    total_quantity: float
    reorder_level: float
    is_low_stock: bool


class StockLedgerOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    warehouse_name: str
    location_name: str
    operation_type: str
    reference_type: str
    reference_id: str
    quantity_before: float
    quantity_change: float
    quantity_after: float
    created_by_name: Optional[str] = None
    created_at: datetime
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# RECEIPTS
# ============================================================================
class ReceiptItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(..., gt=0)
    uom_id: int


class ReceiptItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    quantity: float
    uom_id: int
    uom_code: str

    model_config = ConfigDict(from_attributes=True)


class ReceiptCreate(BaseModel):
    receipt_number: Optional[str] = None
    supplier_id: int
    warehouse_id: int
    destination_location_id: int
    scheduled_at: Optional[datetime] = None
    items: List[ReceiptItemCreate]


class ReceiptOut(BaseModel):
    id: int
    receipt_number: str
    supplier_id: int
    supplier_name: str
    warehouse_id: int
    warehouse_name: str
    destination_location_id: int
    destination_location_name: str
    status: str  # DRAFT, WAITING, READY, DONE, CANCELED
    scheduled_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    created_at: datetime
    validated_at: Optional[datetime] = None
    total_items: int = 0
    total_quantity: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class ReceiptDetailOut(ReceiptOut):
    items: List[ReceiptItemOut] = []


# ============================================================================
# DELIVERIES
# ============================================================================
class DeliveryItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(..., gt=0)
    uom_id: int


class DeliveryItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    quantity: float
    uom_id: int
    uom_code: str
    picked_quantity: float = 0.0
    packed_quantity: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class DeliveryCreate(BaseModel):
    delivery_number: Optional[str] = None
    customer_id: int
    warehouse_id: int
    source_location_id: int
    scheduled_at: Optional[datetime] = None
    items: List[DeliveryItemCreate]


class DeliveryOut(BaseModel):
    id: int
    delivery_number: str
    customer_id: int
    customer_name: str
    warehouse_id: int
    warehouse_name: str
    source_location_id: int
    source_location_name: str
    status: str  # DRAFT, WAITING, READY, DONE, CANCELED
    scheduled_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    created_at: datetime
    validated_at: Optional[datetime] = None
    total_items: int = 0
    total_quantity: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class DeliveryDetailOut(DeliveryOut):
    items: List[DeliveryItemOut] = []


# ============================================================================
# TRANSFERS
# ============================================================================
class TransferItemCreate(BaseModel):
    product_id: int
    quantity: float = Field(..., gt=0)
    uom_id: int


class TransferItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    quantity: float
    uom_id: int
    uom_code: str

    model_config = ConfigDict(from_attributes=True)


class TransferCreate(BaseModel):
    transfer_number: Optional[str] = None
    warehouse_id: int
    source_location_id: int
    destination_location_id: int
    scheduled_at: Optional[datetime] = None
    items: List[TransferItemCreate]


class TransferOut(BaseModel):
    id: int
    transfer_number: str
    warehouse_id: int
    warehouse_name: str
    source_location_id: int
    source_location_name: str
    destination_location_id: int
    destination_location_name: str
    status: str  # DRAFT, WAITING, READY, DONE, CANCELED
    scheduled_at: Optional[datetime] = None
    created_by_name: Optional[str] = None
    created_at: datetime
    validated_at: Optional[datetime] = None
    total_items: int = 0
    total_quantity: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class TransferDetailOut(TransferOut):
    items: List[TransferItemOut] = []


# ============================================================================
# ADJUSTMENTS
# ============================================================================
class AdjustmentItemCreate(BaseModel):
    product_id: int
    counted_quantity: float = Field(..., ge=0)


class AdjustmentItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    system_quantity: float
    counted_quantity: float
    difference: float

    model_config = ConfigDict(from_attributes=True)


class AdjustmentCreate(BaseModel):
    adjustment_number: Optional[str] = None
    warehouse_id: int
    location_id: int
    reason: Optional[str] = None
    items: List[AdjustmentItemCreate]


class AdjustmentOut(BaseModel):
    id: int
    adjustment_number: str
    warehouse_id: int
    warehouse_name: str
    location_id: int
    location_name: str
    status: str  # DRAFT, WAITING, READY, DONE, CANCELED
    reason: Optional[str] = None
    created_by_name: Optional[str] = None
    created_at: datetime
    validated_at: Optional[datetime] = None
    total_items: int = 0

    model_config = ConfigDict(from_attributes=True)


class AdjustmentDetailOut(AdjustmentOut):
    items: List[AdjustmentItemOut] = []
