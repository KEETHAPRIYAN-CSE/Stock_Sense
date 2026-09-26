from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class StockBalance(Base):
    __tablename__ = "stock_balances"
    __table_args__ = (
        UniqueConstraint("product_id", "location_id", name="uq_stock_balance_product_location"),
        Index("ix_stock_balances_product_location", "product_id", "location_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Float, default=0.0, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    product = relationship("Product", back_populates="balances")
    location = relationship("Location", back_populates="balances")


class StockLedger(Base):
    __tablename__ = "stock_ledger"
    __table_args__ = (
        Index("ix_stock_ledger_product", "product_id"),
        Index("ix_stock_ledger_location", "location_id"),
        Index("ix_stock_ledger_created_at", "created_at"),
        Index("ix_stock_ledger_ref", "reference_type", "reference_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="RESTRICT"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="RESTRICT"), nullable=False)
    operation_type = Column(String(50), nullable=False, index=True)  # INITIAL, RECEIPT, DELIVERY, TRANSFER_OUT, TRANSFER_IN, ADJUSTMENT
    reference_type = Column(String(50), nullable=False)  # RECEIPT, DELIVERY, TRANSFER, ADJUSTMENT, INITIAL
    reference_id = Column(String(100), nullable=False)  # Document number or ID
    quantity_before = Column(Float, nullable=False)
    quantity_change = Column(Float, nullable=False)
    quantity_after = Column(Float, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    product = relationship("Product", back_populates="ledger_entries")
    warehouse = relationship("Warehouse", back_populates="ledger_entries")
    location = relationship("Location", back_populates="ledger_entries")
    user = relationship("User")
