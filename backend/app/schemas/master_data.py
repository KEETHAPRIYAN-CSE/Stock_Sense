from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# CATEGORY
# ============================================================================
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# UOM
# ============================================================================
class UOMBase(BaseModel):
    name: str = Field(..., max_length=50)
    code: str = Field(..., max_length=20)
    is_active: bool = True


class UOMCreate(UOMBase):
    pass


class UOMOut(UOMBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# WAREHOUSE
# ============================================================================
class WarehouseBase(BaseModel):
    name: str = Field(..., max_length=150)
    code: str = Field(..., max_length=50)
    address: Optional[str] = None
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class WarehouseOut(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# LOCATION
# ============================================================================
class LocationBase(BaseModel):
    warehouse_id: int
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    location_type: str = "STORAGE"  # STORAGE, PRODUCTION, DISPATCH, RECEIVING
    is_active: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    location_type: Optional[str] = None
    is_active: Optional[bool] = None


class LocationOut(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    warehouse_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# SUPPLIER
# ============================================================================
class SupplierBase(BaseModel):
    name: str = Field(..., max_length=150)
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierOut(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# CUSTOMER
# ============================================================================
class CustomerBase(BaseModel):
    name: str = Field(..., max_length=150)
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class CustomerOut(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# PRODUCT
# ============================================================================
class ProductBase(BaseModel):
    name: str = Field(..., max_length=200)
    sku: str = Field(..., max_length=100)
    category_id: Optional[int] = None
    uom_id: int
    initial_stock: float = 0.0
    reorder_level: float = 0.0
    is_active: bool = True


class ProductCreate(ProductBase):
    initial_warehouse_id: Optional[int] = None
    initial_location_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    uom_id: Optional[int] = None
    reorder_level: Optional[float] = None
    is_active: Optional[bool] = None


class ProductStockByLocation(BaseModel):
    location_id: int
    location_name: str
    warehouse_name: str
    quantity: float

    model_config = ConfigDict(from_attributes=True)


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    uom_code: Optional[str] = None
    uom_name: Optional[str] = None
    total_stock: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class ProductDetailOut(ProductOut):
    location_stocks: List[ProductStockByLocation] = []
