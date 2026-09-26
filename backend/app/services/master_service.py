from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.master_data import Category, Customer, Location, Product, Supplier, UOM, Warehouse
from app.models.stock import StockBalance, StockLedger
from app.repositories.master_repo import MasterRepository
from app.schemas.master_data import (
    CategoryCreate,
    CategoryUpdate,
    CustomerCreate,
    CustomerUpdate,
    LocationCreate,
    LocationUpdate,
    ProductCreate,
    ProductDetailOut,
    ProductOut,
    ProductStockByLocation,
    ProductUpdate,
    SupplierCreate,
    SupplierUpdate,
    UOMCreate,
    WarehouseCreate,
    WarehouseUpdate,
)


class MasterService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MasterRepository(db)

    # ------------------------------------------------------------------------
    # Categories
    # ------------------------------------------------------------------------
    def list_categories(self) -> List[Category]:
        return self.repo.list_categories()

    def create_category(self, data: CategoryCreate) -> Category:
        existing = self.repo.get_category_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category '{data.name}' already exists.",
            )
        return self.repo.create_category(name=data.name, description=data.description)

    def update_category(self, category_id: int, data: CategoryUpdate) -> Category:
        cat = self.repo.get_category_by_id(category_id)
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        return self.repo.update_category(cat, data.model_dump(exclude_unset=True))

    # ------------------------------------------------------------------------
    # UOM
    # ------------------------------------------------------------------------
    def list_uoms(self) -> List[UOM]:
        return self.repo.list_uoms()

    def create_uom(self, data: UOMCreate) -> UOM:
        existing = self.repo.get_uom_by_code(data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"UOM code '{data.code}' already exists.",
            )
        return self.repo.create_uom(name=data.name, code=data.code)

    # ------------------------------------------------------------------------
    # Warehouses
    # ------------------------------------------------------------------------
    def list_warehouses(self) -> List[Warehouse]:
        return self.repo.list_warehouses()

    def get_warehouse(self, warehouse_id: int) -> Warehouse:
        wh = self.repo.get_warehouse_by_id(warehouse_id)
        if not wh:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found"
            )
        return wh

    def create_warehouse(self, data: WarehouseCreate) -> Warehouse:
        existing = self.repo.get_warehouse_by_code(data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Warehouse code '{data.code}' already exists.",
            )
        return self.repo.create_warehouse(
            name=data.name, code=data.code, address=data.address
        )

    def update_warehouse(self, warehouse_id: int, data: WarehouseUpdate) -> Warehouse:
        wh = self.get_warehouse(warehouse_id)
        return self.repo.update_warehouse(wh, data.model_dump(exclude_unset=True))

    # ------------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------------
    def list_locations(self, warehouse_id: Optional[int] = None) -> List[Location]:
        return self.repo.list_locations(warehouse_id=warehouse_id)

    def get_location(self, location_id: int) -> Location:
        loc = self.repo.get_location_by_id(location_id)
        if not loc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
            )
        return loc

    def create_location(self, data: LocationCreate) -> Location:
        self.get_warehouse(data.warehouse_id)
        existing = self.repo.get_location_by_code(data.warehouse_id, data.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Location code '{data.code}' already exists in this warehouse.",
            )
        return self.repo.create_location(
            warehouse_id=data.warehouse_id,
            name=data.name,
            code=data.code,
            location_type=data.location_type,
        )

    def update_location(self, location_id: int, data: LocationUpdate) -> Location:
        loc = self.get_location(location_id)
        return self.repo.update_location(loc, data.model_dump(exclude_unset=True))

    # ------------------------------------------------------------------------
    # Suppliers & Customers
    # ------------------------------------------------------------------------
    def list_suppliers(self) -> List[Supplier]:
        return self.repo.list_suppliers()

    def create_supplier(self, data: SupplierCreate) -> Supplier:
        return self.repo.create_supplier(data.model_dump())

    def update_supplier(self, supplier_id: int, data: SupplierUpdate) -> Supplier:
        supplier = self.repo.get_supplier_by_id(supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
            )
        return self.repo.update_supplier(supplier, data.model_dump(exclude_unset=True))

    def list_customers(self) -> List[Customer]:
        return self.repo.list_customers()

    def create_customer(self, data: CustomerCreate) -> Customer:
        return self.repo.create_customer(data.model_dump())

    def update_customer(self, customer_id: int, data: CustomerUpdate) -> Customer:
        customer = self.repo.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )
        return self.repo.update_customer(customer, data.model_dump(exclude_unset=True))

    # ------------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------------
    def list_products(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        active_only: bool = False,
    ) -> List[ProductOut]:
        products = self.repo.list_products(
            search=search, category_id=category_id, active_only=active_only
        )
        result = []
        for p in products:
            total_qty = self.repo.get_product_total_stock(p.id)
            result.append(
                ProductOut(
                    id=p.id,
                    name=p.name,
                    sku=p.sku,
                    category_id=p.category_id,
                    uom_id=p.uom_id,
                    initial_stock=p.initial_stock,
                    reorder_level=p.reorder_level,
                    is_active=p.is_active,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                    category_name=p.category.name if p.category else None,
                    uom_code=p.uom.code if p.uom else None,
                    uom_name=p.uom.name if p.uom else None,
                    total_stock=total_qty,
                )
            )
        return result

    def get_product_detail(self, product_id: int) -> ProductDetailOut:
        p = self.repo.get_product_by_id(product_id)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        balances = self.repo.get_product_location_stocks(product_id)
        loc_stocks = [
            ProductStockByLocation(
                location_id=b.location_id,
                location_name=b.location.name,
                warehouse_name=b.location.warehouse.name,
                quantity=b.quantity,
            )
            for b in balances
        ]
        total_qty = sum(b.quantity for b in balances)

        return ProductDetailOut(
            id=p.id,
            name=p.name,
            sku=p.sku,
            category_id=p.category_id,
            uom_id=p.uom_id,
            initial_stock=p.initial_stock,
            reorder_level=p.reorder_level,
            is_active=p.is_active,
            created_at=p.created_at,
            updated_at=p.updated_at,
            category_name=p.category.name if p.category else None,
            uom_code=p.uom.code if p.uom else None,
            uom_name=p.uom.name if p.uom else None,
            total_stock=total_qty,
            location_stocks=loc_stocks,
        )

    def create_product(self, data: ProductCreate, user_id: Optional[int] = None) -> ProductOut:
        existing = self.repo.get_product_by_sku(data.sku)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product SKU '{data.sku}' already exists.",
            )

        uom = self.repo.get_uom_by_id(data.uom_id)
        if not uom:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UOM specified."
            )

        prod_data = data.model_dump(
            exclude={"initial_warehouse_id", "initial_location_id"}
        )
        product = self.repo.create_product(prod_data)

        # If initial stock and initial location were provided, initialize stock balance and ledger
        if data.initial_stock > 0 and data.initial_location_id:
            loc = self.repo.get_location_by_id(data.initial_location_id)
            if loc:
                balance = StockBalance(
                    product_id=product.id,
                    location_id=loc.id,
                    quantity=data.initial_stock,
                )
                self.db.add(balance)

                ledger = StockLedger(
                    product_id=product.id,
                    warehouse_id=loc.warehouse_id,
                    location_id=loc.id,
                    operation_type="INITIAL",
                    reference_type="INITIAL",
                    reference_id=f"INIT-{product.sku}",
                    quantity_before=0.0,
                    quantity_change=data.initial_stock,
                    quantity_after=data.initial_stock,
                    created_by=user_id,
                    notes="Initial product stock on creation",
                )
                self.db.add(ledger)
                self.db.commit()

        return self.get_product_detail(product.id)

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductOut:
        p = self.repo.get_product_by_id(product_id)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        self.repo.update_product(p, data.model_dump(exclude_unset=True))
        return self.get_product_detail(product_id)

    def delete_product(self, product_id: int) -> None:
        p = self.repo.get_product_by_id(product_id)
        if not p:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        self.repo.delete_product(p)
