from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.database import Base, engine, SessionLocal
from app.core.security import get_password_hash
import app.models  # Ensure all models are imported
from app.models import (
    Adjustment,
    AdjustmentItem,
    Category,
    Customer,
    Delivery,
    DeliveryItem,
    Location,
    Product,
    Receipt,
    ReceiptItem,
    StockBalance,
    StockLedger,
    Supplier,
    Transfer,
    TransferItem,
    UOM,
    User,
    Warehouse,
)


def get_or_create(session: Session, model, defaults=None, **lookup):
    instance = session.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    params = {**lookup, **(defaults or {})}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance, True


def init_db() -> None:
    """Initialize database tables and seed baseline real enterprise operational data."""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        # Seed or sync Manager account
        manager = db.query(User).filter_by(email="manager@stocksense.com").first()
        if not manager:
            manager = User(
                email="manager@stocksense.com",
                full_name="Inventory Manager",
                password_hash=get_password_hash("admin123"),
                role="INVENTORY_MANAGER",
                is_active=True,
            )
            db.add(manager)
            db.flush()
        else:
            manager.password_hash = get_password_hash("admin123")
            manager.is_active = True

        # Seed or sync Staff account
        staff = db.query(User).filter_by(email="staff@stocksense.com").first()
        if not staff:
            staff = User(
                email="staff@stocksense.com",
                full_name="Warehouse Staff",
                password_hash=get_password_hash("staff123"),
                role="WAREHOUSE_STAFF",
                is_active=True,
            )
            db.add(staff)
            db.flush()
        else:
            staff.password_hash = get_password_hash("staff123")
            staff.is_active = True

        # Seed Categories
        raw, _ = get_or_create(db, Category, name="Raw Materials", defaults={"description": "High-grade industrial metals and alloys"})
        finished, _ = get_or_create(db, Category, name="Finished Goods", defaults={"description": "Completed manufacturing inventory and commercial furniture"})
        components, _ = get_or_create(db, Category, name="Components & Hardware", defaults={"description": "Mechanical fasteners, structural brackets, and assembly components"})
        electronics, _ = get_or_create(db, Category, name="Electrical & Sensors", defaults={"description": "Industrial sensors, circuit modules, and cabling"})

        # Seed UOMs
        kg, _ = get_or_create(db, UOM, code="kg", defaults={"name": "Kilogram"})
        pcs, _ = get_or_create(db, UOM, code="pcs", defaults={"name": "Piece"})
        box, _ = get_or_create(db, UOM, code="box", defaults={"name": "Box (100 units)"})
        m, _ = get_or_create(db, UOM, code="m", defaults={"name": "Meter"})
        pallet, _ = get_or_create(db, UOM, code="plt", defaults={"name": "Pallet"})

        # Seed Warehouses
        main_wh, _ = get_or_create(
            db,
            Warehouse,
            code="WH-MAIN",
            defaults={"name": "Central Logistics Hub", "address": "Bay 14, Industrial Corridor, Coimbatore"},
        )
        sat_wh, _ = get_or_create(
            db,
            Warehouse,
            code="WH-SAT",
            defaults={"name": "North Distribution Center", "address": "Dock 4, Express Freight Way, Bangalore"},
        )

        # Seed Locations
        main_store, _ = get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="LOC-MS-01",
            defaults={"name": "Main Raw Storage Bay A", "location_type": "STORAGE"},
        )
        prod_rack, _ = get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="LOC-PR-02",
            defaults={"name": "Assembly Staging Line 1", "location_type": "PRODUCTION"},
        )
        fg_bay, _ = get_or_create(
            db,
            Location,
            warehouse_id=main_wh.id,
            code="LOC-FG-03",
            defaults={"name": "Finished Goods Shipping Deck", "location_type": "STORAGE"},
        )
        sat_bay, _ = get_or_create(
            db,
            Location,
            warehouse_id=sat_wh.id,
            code="LOC-SAT-01",
            defaults={"name": "Satellite Transit Buffer", "location_type": "STORAGE"},
        )

        # Seed Suppliers
        sup1, _ = get_or_create(
            db,
            Supplier,
            name="Apex Precision Steel Ltd",
            defaults={"contact_name": "Asha Rao", "email": "procurement@apexsteel.example.com", "phone": "+91 98401 12345"},
        )
        sup2, _ = get_or_create(
            db,
            Supplier,
            name="BoltWorks Fasteners Co",
            defaults={"contact_name": "Imran Khan", "email": "orders@boltworks.example.com", "phone": "+91 97890 23456"},
        )
        sup3, _ = get_or_create(
            db,
            Supplier,
            name="Nova Electronics Systems",
            defaults={"contact_name": "David Chen", "email": "supply@novasystems.example.com", "phone": "+91 94430 34567"},
        )

        # Seed Customers
        cust1, _ = get_or_create(
            db,
            Customer,
            name="Titan Heavy Machinery Ltd",
            defaults={"email": "logistics@titanmachinery.example.com", "phone": "+91 99400 54321", "address": "Plant 7, Outer Ring Road, Chennai"},
        )
        cust2, _ = get_or_create(
            db,
            Customer,
            name="Urban Habitat Interiors",
            defaults={"email": "fulfillment@urbanhabitat.example.com", "phone": "+91 98840 65432", "address": "Plot 12, Export Promotion Park, Kochi"},
        )
        cust3, _ = get_or_create(
            db,
            Customer,
            name="Metro Rail Infrastructure Corp",
            defaults={"email": "inventory@metrorail.example.com", "phone": "+91 97710 76543", "address": "Depot 3, Central Metro Hub, Hyderabad"},
        )

        # Seed Comprehensive Enterprise Products
        product_data = [
            ("Structural Steel Beams 316L", "SKU-STL-316", raw.id, kg.id, 450.0, 50.0, main_store.id, main_wh.id),
            ("High-Tensile Hex Bolts M12x50", "SKU-BLT-M12", components.id, box.id, 120.0, 25.0, main_store.id, main_wh.id),
            ("Executive Ergonomic Mesh Chairs", "SKU-CHR-EXEC", finished.id, pcs.id, 65.0, 15.0, fg_bay.id, main_wh.id),
            ("Modular Steel Subframes 2x1m", "SKU-FRM-201", finished.id, pcs.id, 4.0, 12.0, prod_rack.id, main_wh.id),  # Low Stock intentionally
            ("Optical Proximity Sensors 24V", "SKU-SNS-OPT", electronics.id, pcs.id, 80.0, 20.0, main_store.id, main_wh.id),
            ("Heavy-Duty Industrial Casters", "SKU-CST-880", components.id, pcs.id, 0.0, 10.0, main_store.id, main_wh.id),   # Out of Stock intentionally
        ]

        seeded_products = {}
        for name, sku, cat_id, uom_id, stock_qty, reorder, loc_id, wh_id in product_data:
            product, created = get_or_create(
                db,
                Product,
                sku=sku,
                defaults={
                    "name": name,
                    "category_id": cat_id,
                    "uom_id": uom_id,
                    "initial_stock": stock_qty,
                    "reorder_level": reorder,
                    "is_active": True,
                },
            )
            seeded_products[sku] = product
            
            # Upsert Stock Balance
            bal = db.query(StockBalance).filter_by(product_id=product.id, location_id=loc_id).first()
            if not bal:
                bal = StockBalance(product_id=product.id, location_id=loc_id, quantity=stock_qty)
                db.add(bal)
            else:
                bal.quantity = stock_qty

            # Upsert Stock Ledger Entry
            ledger_entry = db.query(StockLedger).filter_by(reference_id=f"INIT-{sku}").first()
            if not ledger_entry:
                db.add(
                    StockLedger(
                        product_id=product.id,
                        warehouse_id=wh_id,
                        location_id=loc_id,
                        operation_type="INITIAL",
                        reference_type="INITIAL",
                        reference_id=f"INIT-{sku}",
                        quantity_before=0.0,
                        quantity_change=stock_qty,
                        quantity_after=stock_qty,
                        created_by=manager.id,
                        notes=f"Opening warehouse balance for {name}",
                    )
                )

        # Seed Receipts (1 DONE, 1 READY, 1 DRAFT)
        r1, r1_created = get_or_create(
            db,
            Receipt,
            receipt_number="REC-2026-0001",
            defaults={
                "supplier_id": sup1.id,
                "warehouse_id": main_wh.id,
                "destination_location_id": main_store.id,
                "status": "DONE",
                "created_by": manager.id,
                "validated_by": manager.id,
                "validated_at": datetime.now(timezone.utc),
            },
        )
        if r1_created:
            db.add(ReceiptItem(receipt_id=r1.id, product_id=seeded_products["SKU-STL-316"].id, quantity=250.0, uom_id=kg.id))
            db.add(ReceiptItem(receipt_id=r1.id, product_id=seeded_products["SKU-BLT-M12"].id, quantity=50.0, uom_id=box.id))

        r2, r2_created = get_or_create(
            db,
            Receipt,
            receipt_number="REC-2026-0002",
            defaults={
                "supplier_id": sup3.id,
                "warehouse_id": main_wh.id,
                "destination_location_id": main_store.id,
                "status": "READY",
                "created_by": staff.id,
            },
        )
        if r2_created:
            db.add(ReceiptItem(receipt_id=r2.id, product_id=seeded_products["SKU-SNS-OPT"].id, quantity=40.0, uom_id=pcs.id))

        r3, r3_created = get_or_create(
            db,
            Receipt,
            receipt_number="REC-2026-0003",
            defaults={
                "supplier_id": sup2.id,
                "warehouse_id": main_wh.id,
                "destination_location_id": main_store.id,
                "status": "DRAFT",
                "created_by": manager.id,
            },
        )
        if r3_created:
            db.add(ReceiptItem(receipt_id=r3.id, product_id=seeded_products["SKU-CST-880"].id, quantity=30.0, uom_id=pcs.id))

        # Seed Deliveries (1 DONE, 1 READY, 1 DRAFT)
        d1, d1_created = get_or_create(
            db,
            Delivery,
            delivery_number="DEL-2026-0001",
            defaults={
                "customer_id": cust1.id,
                "warehouse_id": main_wh.id,
                "source_location_id": fg_bay.id,
                "status": "DONE",
                "created_by": manager.id,
                "validated_by": manager.id,
                "validated_at": datetime.now(timezone.utc),
            },
        )
        if d1_created:
            db.add(DeliveryItem(delivery_id=d1.id, product_id=seeded_products["SKU-CHR-EXEC"].id, quantity=15.0, uom_id=pcs.id))

        d2, d2_created = get_or_create(
            db,
            Delivery,
            delivery_number="DEL-2026-0002",
            defaults={
                "customer_id": cust2.id,
                "warehouse_id": main_wh.id,
                "source_location_id": fg_bay.id,
                "status": "READY",
                "created_by": staff.id,
            },
        )
        if d2_created:
            db.add(DeliveryItem(delivery_id=d2.id, product_id=seeded_products["SKU-CHR-EXEC"].id, quantity=10.0, uom_id=pcs.id))

        # Seed Internal Transfer (DONE)
        t1, t1_created = get_or_create(
            db,
            Transfer,
            transfer_number="TRF-2026-0001",
            defaults={
                "warehouse_id": main_wh.id,
                "source_location_id": main_store.id,
                "destination_location_id": prod_rack.id,
                "status": "DONE",
                "created_by": manager.id,
                "validated_by": manager.id,
                "validated_at": datetime.now(timezone.utc),
            },
        )
        if t1_created:
            db.add(TransferItem(transfer_id=t1.id, product_id=seeded_products["SKU-STL-316"].id, quantity=50.0, uom_id=kg.id))

        # Seed Stock Adjustment (DONE)
        a1, a1_created = get_or_create(
            db,
            Adjustment,
            adjustment_number="ADJ-2026-0001",
            defaults={
                "warehouse_id": main_wh.id,
                "location_id": main_store.id,
                "reason": "Annual cycle count reconciliation audit",
                "status": "DONE",
                "created_by": manager.id,
                "validated_by": manager.id,
                "validated_at": datetime.now(timezone.utc),
            },
        )
        if a1_created:
            db.add(
                AdjustmentItem(
                    adjustment_id=a1.id,
                    product_id=seeded_products["SKU-BLT-M12"].id,
                    system_quantity=115.0,
                    counted_quantity=120.0,
                    difference=5.0,
                )
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
