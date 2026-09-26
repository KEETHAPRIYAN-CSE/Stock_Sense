from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.user import User
from app.schemas.master_data import (
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
    LocationCreate,
    LocationOut,
    LocationUpdate,
    ProductCreate,
    ProductDetailOut,
    ProductOut,
    ProductUpdate,
    SupplierCreate,
    SupplierOut,
    SupplierUpdate,
    UOMCreate,
    UOMOut,
    WarehouseCreate,
    WarehouseOut,
    WarehouseUpdate,
)
from app.services.master_service import MasterService

router = APIRouter(tags=["Master Data"])


# ============================================================================
# PRODUCTS
# ============================================================================
@router.get("/products", response_model=List[ProductOut])
def list_products(
    search: Optional[str] = Query(None, description="Search by product name or SKU"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    active_only: bool = Query(False, description="Filter only active products"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_products(search=search, category_id=category_id, active_only=active_only)


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_product(product_in, user_id=current_user.id)


@router.get("/products/{product_id}", response_model=ProductDetailOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.get_product_detail(product_id)


@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.update_product(product_id, product_in)


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    service.delete_product(product_id)
    return {"message": "Product deactivated successfully"}


# ============================================================================
# CATEGORIES
# ============================================================================
@router.get("/categories", response_model=List[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_categories()


@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_category(cat_in)


@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    cat_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.update_category(category_id, cat_in)


# ============================================================================
# UOMS
# ============================================================================
@router.get("/uoms", response_model=List[UOMOut])
def list_uoms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_uoms()


@router.post("/uoms", response_model=UOMOut, status_code=status.HTTP_201_CREATED)
def create_uom(
    uom_in: UOMCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_uom(uom_in)


# ============================================================================
# WAREHOUSES
# ============================================================================
@router.get("/warehouses", response_model=List[WarehouseOut])
def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_warehouses()


@router.post("/warehouses", response_model=WarehouseOut, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    wh_in: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_warehouse(wh_in)


@router.put("/warehouses/{warehouse_id}", response_model=WarehouseOut)
def update_warehouse(
    warehouse_id: int,
    wh_in: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.update_warehouse(warehouse_id, wh_in)


# ============================================================================
# LOCATIONS
# ============================================================================
@router.get("/locations", response_model=List[LocationOut])
def list_locations(
    warehouse_id: Optional[int] = Query(None, description="Filter locations by warehouse"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    locations = service.list_locations(warehouse_id=warehouse_id)
    return [
        LocationOut(
            id=loc.id,
            warehouse_id=loc.warehouse_id,
            name=loc.name,
            code=loc.code,
            location_type=loc.location_type,
            is_active=loc.is_active,
            created_at=loc.created_at,
            updated_at=loc.updated_at,
            warehouse_name=loc.warehouse.name if loc.warehouse else None,
        )
        for loc in locations
    ]


@router.post("/locations", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(
    loc_in: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    loc = service.create_location(loc_in)
    return LocationOut(
        id=loc.id,
        warehouse_id=loc.warehouse_id,
        name=loc.name,
        code=loc.code,
        location_type=loc.location_type,
        is_active=loc.is_active,
        created_at=loc.created_at,
        updated_at=loc.updated_at,
        warehouse_name=loc.warehouse.name if loc.warehouse else None,
    )


@router.put("/locations/{location_id}", response_model=LocationOut)
def update_location(
    location_id: int,
    loc_in: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    loc = service.update_location(location_id, loc_in)
    return LocationOut(
        id=loc.id,
        warehouse_id=loc.warehouse_id,
        name=loc.name,
        code=loc.code,
        location_type=loc.location_type,
        is_active=loc.is_active,
        created_at=loc.created_at,
        updated_at=loc.updated_at,
        warehouse_name=loc.warehouse.name if loc.warehouse else None,
    )


# ============================================================================
# SUPPLIERS
# ============================================================================
@router.get("/suppliers", response_model=List[SupplierOut])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_suppliers()


@router.post("/suppliers", response_model=SupplierOut, status_code=status.HTTP_201_CREATED)
def create_supplier(
    sup_in: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_supplier(sup_in)


@router.put("/suppliers/{supplier_id}", response_model=SupplierOut)
def update_supplier(
    supplier_id: int,
    sup_in: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.update_supplier(supplier_id, sup_in)


# ============================================================================
# CUSTOMERS
# ============================================================================
@router.get("/customers", response_model=List[CustomerOut])
def list_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.list_customers()


@router.post("/customers", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    cust_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.create_customer(cust_in)


@router.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: int,
    cust_in: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MasterService(db)
    return service.update_customer(customer_id, cust_in)
