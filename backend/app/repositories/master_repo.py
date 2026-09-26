from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.master_data import (
    Category,
    Customer,
    Location,
    Product,
    Supplier,
    UOM,
    Warehouse,
)
from app.models.stock import StockBalance


class MasterRepository:
    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------------
    # Categories
    # ------------------------------------------------------------------------
    def list_categories(self, active_only: bool = False) -> List[Category]:
        q = self.db.query(Category)
        if active_only:
            q = q.filter(Category.is_active.is_(True))
        return q.order_by(Category.name).all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_category_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name.ilike(name.strip())).first()

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        cat = Category(name=name.strip(), description=description)
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update_category(self, cat: Category, data: dict) -> Category:
        for key, val in data.items():
            if val is not None:
                setattr(cat, key, val)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    # ------------------------------------------------------------------------
    # UOMs
    # ------------------------------------------------------------------------
    def list_uoms(self) -> List[UOM]:
        return self.db.query(UOM).filter(UOM.is_active.is_(True)).order_by(UOM.name).all()

    def get_uom_by_code(self, code: str) -> Optional[UOM]:
        return self.db.query(UOM).filter(UOM.code.ilike(code.strip())).first()

    def get_uom_by_id(self, uom_id: int) -> Optional[UOM]:
        return self.db.query(UOM).filter(UOM.id == uom_id).first()

    def create_uom(self, name: str, code: str) -> UOM:
        uom = UOM(name=name.strip(), code=code.strip().lower())
        self.db.add(uom)
        self.db.commit()
        self.db.refresh(uom)
        return uom

    # ------------------------------------------------------------------------
    # Warehouses
    # ------------------------------------------------------------------------
    def list_warehouses(self, active_only: bool = False) -> List[Warehouse]:
        q = self.db.query(Warehouse)
        if active_only:
            q = q.filter(Warehouse.is_active.is_(True))
        return q.order_by(Warehouse.name).all()

    def get_warehouse_by_id(self, warehouse_id: int) -> Optional[Warehouse]:
        return self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    def get_warehouse_by_code(self, code: str) -> Optional[Warehouse]:
        return self.db.query(Warehouse).filter(Warehouse.code.ilike(code.strip())).first()

    def create_warehouse(self, name: str, code: str, address: Optional[str] = None) -> Warehouse:
        wh = Warehouse(name=name.strip(), code=code.strip().upper(), address=address)
        self.db.add(wh)
        self.db.commit()
        self.db.refresh(wh)
        return wh

    def update_warehouse(self, wh: Warehouse, data: dict) -> Warehouse:
        for key, val in data.items():
            if val is not None:
                setattr(wh, key, val)
        self.db.commit()
        self.db.refresh(wh)
        return wh

    # ------------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------------
    def list_locations(self, warehouse_id: Optional[int] = None) -> List[Location]:
        q = self.db.query(Location)
        if warehouse_id is not None:
            q = q.filter(Location.warehouse_id == warehouse_id)
        return q.order_by(Location.name).all()

    def get_location_by_id(self, location_id: int) -> Optional[Location]:
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_location_by_code(self, warehouse_id: int, code: str) -> Optional[Location]:
        return (
            self.db.query(Location)
            .filter(Location.warehouse_id == warehouse_id, Location.code.ilike(code.strip()))
            .first()
        )

    def create_location(
        self, warehouse_id: int, name: str, code: str, location_type: str = "STORAGE"
    ) -> Location:
        loc = Location(
            warehouse_id=warehouse_id,
            name=name.strip(),
            code=code.strip().upper(),
            location_type=location_type,
        )
        self.db.add(loc)
        self.db.commit()
        self.db.refresh(loc)
        return loc

    def update_location(self, loc: Location, data: dict) -> Location:
        for key, val in data.items():
            if val is not None:
                setattr(loc, key, val)
        self.db.commit()
        self.db.refresh(loc)
        return loc

    # ------------------------------------------------------------------------
    # Suppliers
    # ------------------------------------------------------------------------
    def list_suppliers(self) -> List[Supplier]:
        return self.db.query(Supplier).order_by(Supplier.name).all()

    def get_supplier_by_id(self, supplier_id: int) -> Optional[Supplier]:
        return self.db.query(Supplier).filter(Supplier.id == supplier_id).first()

    def create_supplier(self, data: dict) -> Supplier:
        supplier = Supplier(**data)
        self.db.add(supplier)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    def update_supplier(self, supplier: Supplier, data: dict) -> Supplier:
        for key, val in data.items():
            if val is not None:
                setattr(supplier, key, val)
        self.db.commit()
        self.db.refresh(supplier)
        return supplier

    # ------------------------------------------------------------------------
    # Customers
    # ------------------------------------------------------------------------
    def list_customers(self) -> List[Customer]:
        return self.db.query(Customer).order_by(Customer.name).all()

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()

    def create_customer(self, data: dict) -> Customer:
        customer = Customer(**data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update_customer(self, customer: Customer, data: dict) -> Customer:
        for key, val in data.items():
            if val is not None:
                setattr(customer, key, val)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    # ------------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------------
    def list_products(
        self,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        active_only: bool = False,
    ) -> List[Product]:
        q = self.db.query(Product)
        if active_only:
            q = q.filter(Product.is_active.is_(True))
        if category_id:
            q = q.filter(Product.category_id == category_id)
        if search:
            pattern = f"%{search.strip()}%"
            q = q.filter((Product.name.ilike(pattern)) | (Product.sku.ilike(pattern)))
        return q.order_by(Product.name).all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.sku.ilike(sku.strip())).first()

    def get_product_total_stock(self, product_id: int) -> float:
        result = (
            self.db.query(func.coalesce(func.sum(StockBalance.quantity), 0.0))
            .filter(StockBalance.product_id == product_id)
            .scalar()
        )
        return float(result or 0.0)

    def get_product_location_stocks(self, product_id: int) -> List[StockBalance]:
        return (
            self.db.query(StockBalance)
            .join(Location, StockBalance.location_id == Location.id)
            .filter(StockBalance.product_id == product_id, StockBalance.quantity > 0)
            .all()
        )

    def create_product(self, data: dict) -> Product:
        product = Product(**data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product: Product, data: dict) -> Product:
        for key, val in data.items():
            if val is not None:
                setattr(product, key, val)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product: Product) -> None:
        # Soft-delete by marking inactive
        product.is_active = False
        self.db.commit()
