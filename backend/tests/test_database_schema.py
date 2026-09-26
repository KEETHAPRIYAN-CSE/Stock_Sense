import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models import (
    User,
    PasswordResetOTP,
    Category,
    UOM,
    Product,
    Warehouse,
    Location,
    Supplier,
    Customer,
    StockBalance,
    StockLedger,
    Receipt,
    ReceiptItem,
    Delivery,
    DeliveryItem,
    Transfer,
    TransferItem,
    Adjustment,
    AdjustmentItem,
    ReorderRule,
)


@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_schema_creation(db_session):
    # Verify tables can be instantiated and queried
    user = User(
        full_name="Admin User",
        email="admin@test.com",
        password_hash="hashed_pw",
        role="INVENTORY_MANAGER",
    )
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(email="admin@test.com").first()
    assert saved_user is not None
    assert saved_user.id is not None
    assert saved_user.full_name == "Admin User"


def test_master_data_relationships(db_session):
    category = Category(name="Raw Materials", description="Metals and plastics")
    uom = UOM(name="Kilogram", code="kg")
    db_session.add_all([category, uom])
    db_session.commit()

    product = Product(
        name="Steel Rods",
        sku="ROD-001",
        category_id=category.id,
        uom_id=uom.id,
        initial_stock=100.0,
        reorder_level=20.0,
    )
    db_session.add(product)
    db_session.commit()

    warehouse = Warehouse(name="Main Hub", code="WH-01")
    db_session.add(warehouse)
    db_session.commit()

    location = Location(
        warehouse_id=warehouse.id,
        name="Main Store",
        code="LOC-MS",
        location_type="STORAGE",
    )
    db_session.add(location)
    db_session.commit()

    balance = StockBalance(
        product_id=product.id,
        location_id=location.id,
        quantity=100.0,
    )
    db_session.add(balance)
    db_session.commit()

    retrieved = db_session.query(StockBalance).first()
    assert retrieved.quantity == 100.0
    assert retrieved.product.name == "Steel Rods"
    assert retrieved.location.name == "Main Store"
