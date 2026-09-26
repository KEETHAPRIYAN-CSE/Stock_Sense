"""
Seed StockSense with demo master data.

Run from the backend directory so app imports resolve:

    cd backend
    python ../scripts/seed_database.py
"""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import SessionLocal  # noqa: E402
from app.core.security import get_password_hash  # noqa: E402
from app.models import (  # noqa: E402
    Category,
    Customer,
    Location,
    Product,
    StockBalance,
    StockLedger,
    Supplier,
    UOM,
    User,
    Warehouse,
)


def get_or_create(session, model, defaults=None, **lookup):
    instance = session.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    params = {**lookup, **(defaults or {})}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance, True


def seed() -> None:
    db = SessionLocal()
    try:
        manager, created_manager = get_or_create(
            db,
            User,
            email="manager@stocksense.com",
            defaults={
                "full_name": "Inventory Manager",
                "password_hash": get_password_hash("admin123"),
                "role": "INVENTORY_MANAGER",
                "is_active": True,
            },
        )
        get_or_create(
            db,
            User,
            email="staff@stocksense.com",
            defaults={
                "full_name": "Warehouse Staff",
                "password_hash": get_password_hash("staff123"),
                "role": "WAREHOUSE_STAFF",
                "is_active": True,
            },
        )

        raw, _ = get_or_create(db, Category, name="Raw Materials", defaults={"description": "Incoming raw inputs"})
        finished, _ = get_or_create(db, Category, name="Finished Goods", defaults={"description": "Sellable completed items"})
        components, _ = get_or_create(db, Category, name="Components", defaults={"description": "Assembly parts"})

        kg, _ = get_or_create(db, UOM, code="kg", defaults={"name": "Kilogram"})
        pcs, _ = get_or_create(db, UOM, code="pcs", defaults={"name": "Piece"})
        box, _ = get_or_create(db, UOM, code="box", defaults={"name": "Box"})
        get_or_create(db, UOM, code="m", defaults={"name": "Meter"})

        main_wh, _ = get_or_create(
            db,
            Warehouse,
            code="WH-MAIN",
            defaults={"name": "Main Warehouse", "address": "Industrial Estate, Bay 1"},
        )
        sat_wh, _ = get_or_create(
            db,
            Warehouse,
            code="WH-SAT",
            defaults={"name": "Satellite Warehouse", "address": "North Yard, Dock 4"},
        )

        main_store, _ = get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="MS",
            defaults={"name": "Main Store", "location_type": "STORAGE"},
        )
        prod_rack, _ = get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="PR",
            defaults={"name": "Production Rack", "location_type": "PRODUCTION"},
        )
        get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="RA",
            defaults={"name": "Rack A", "location_type": "STORAGE"},
        )
        get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="RB",
            defaults={"name": "Rack B", "location_type": "STORAGE"},
        )
        get_or_create(
            db,
            Location,
            warehouse_id=sat_wh.id,
            code="SAT-1",
            defaults={"name": "Satellite Bay", "location_type": "STORAGE"},
        )

        get_or_create(
            db,
            Supplier,
            name="Steel Provider Ltd",
            defaults={"contact_name": "Asha Rao", "email": "sales@steelprovider.example", "phone": "+91 90000 11111"},
        )
        get_or_create(
            db,
            Supplier,
            name="BoltWorks Co",
            defaults={"contact_name": "Imran Khan", "email": "orders@boltworks.example", "phone": "+91 90000 22222"},
        )
        get_or_create(
            db,
            Customer,
            name="Heavy Machinery Inc",
            defaults={"email": "recv@heavymach.example", "phone": "+91 80000 11111", "address": "Plant 7, Outer Ring"},
        )
        get_or_create(
            db,
            Customer,
            name="Urban Seating Pvt",
            defaults={"email": "ops@urbanseating.example", "phone": "+91 80000 22222", "address": "Showroom Park, Block C"},
        )

        products = [
            ("Steel Rods", "ROD-001", raw.id, kg.id, 20.0),
            ("Chairs", "CHR-010", finished.id, pcs.id, 10.0),
            ("Bolts", "BLT-220", components.id, box.id, 15.0),
            ("Finished Frames", "FRM-500", finished.id, pcs.id, 8.0),
        ]

        for name, sku, cat_id, uom_id, reorder in products:
            product, created = get_or_create(
                db,
                Product,
                sku=sku,
                defaults={
                    "name": name,
                    "category_id": cat_id,
                    "uom_id": uom_id,
                    "initial_stock": 0.0,
                    "reorder_level": reorder,
                    "is_active": True,
                },
            )
            if created:
                # Leave stock at zero so the live demo can receive 100 kg Steel Rods.
                db.add(
                    StockBalance(
                        product_id=product.id,
                        location_id=main_store.id,
                        quantity=0.0,
                    )
                )
                db.add(
                    StockLedger(
                        product_id=product.id,
                        warehouse_id=main_wh.id,
                        location_id=main_store.id,
                        operation_type="INITIAL",
                        reference_type="INITIAL",
                        reference_id=f"INIT-{sku}",
                        quantity_before=0.0,
                        quantity_change=0.0,
                        quantity_after=0.0,
                        created_by=manager.id,
                        notes="Seeded product with empty opening balance",
                    )
                )

        db.commit()
        print("Seed complete.")
        print("Demo login: manager@stocksense.com / admin123")
        if created_manager:
            print("Created inventory manager account.")
        else:
            print("Inventory manager already existed; passwords were not overwritten.")
        print("Use Main Store and Production Rack for the required demo transfer.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
