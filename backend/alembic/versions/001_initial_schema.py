"""001_initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-26 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='INVENTORY_MANAGER'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    # 2. password_reset_otps
    op.create_table(
        'password_reset_otps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('otp_hash', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('attempt_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_password_reset_otps_id', 'password_reset_otps', ['id'], unique=False)
    op.create_index('ix_password_reset_otps_user_id', 'password_reset_otps', ['user_id'], unique=False)

    # 3. categories
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categories_id', 'categories', ['id'], unique=False)
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)

    # 4. uoms
    op.create_table(
        'uoms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_uoms_code', 'uoms', ['code'], unique=True)
    op.create_index('ix_uoms_id', 'uoms', ['id'], unique=False)

    # 5. products
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('sku', sa.String(length=100), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('uom_id', sa.Integer(), nullable=False),
        sa.Column('initial_stock', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('reorder_level', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['uom_id'], ['uoms.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_products_id', 'products', ['id'], unique=False)
    op.create_index('ix_products_name', 'products', ['name'], unique=False)
    op.create_index('ix_products_sku', 'products', ['sku'], unique=True)
    op.create_index('ix_products_category_id', 'products', ['category_id'], unique=False)

    # 6. warehouses
    op.create_table(
        'warehouses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_warehouses_code', 'warehouses', ['code'], unique=True)
    op.create_index('ix_warehouses_id', 'warehouses', ['id'], unique=False)

    # 7. locations
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('location_type', sa.String(length=50), nullable=False, server_default='STORAGE'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('warehouse_id', 'code', name='uq_location_warehouse_code')
    )
    op.create_index('ix_locations_id', 'locations', ['id'], unique=False)
    op.create_index('ix_locations_warehouse_id', 'locations', ['warehouse_id'], unique=False)

    # 8. suppliers
    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('contact_name', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_suppliers_id', 'suppliers', ['id'], unique=False)
    op.create_index('ix_suppliers_name', 'suppliers', ['name'], unique=False)

    # 9. customers
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_customers_id', 'customers', ['id'], unique=False)
    op.create_index('ix_customers_name', 'customers', ['name'], unique=False)

    # 10. stock_balances
    op.create_table(
        'stock_balances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_id', 'location_id', name='uq_stock_balance_product_location')
    )
    op.create_index('ix_stock_balances_id', 'stock_balances', ['id'], unique=False)
    op.create_index('ix_stock_balances_product_id', 'stock_balances', ['product_id'], unique=False)
    op.create_index('ix_stock_balances_location_id', 'stock_balances', ['location_id'], unique=False)
    op.create_index('ix_stock_balances_product_location', 'stock_balances', ['product_id', 'location_id'], unique=False)

    # 11. stock_ledger
    op.create_table(
        'stock_ledger',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('operation_type', sa.String(length=50), nullable=False),
        sa.Column('reference_type', sa.String(length=50), nullable=False),
        sa.Column('reference_id', sa.String(length=100), nullable=False),
        sa.Column('quantity_before', sa.Float(), nullable=False),
        sa.Column('quantity_change', sa.Float(), nullable=False),
        sa.Column('quantity_after', sa.Float(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_stock_ledger_id', 'stock_ledger', ['id'], unique=False)
    op.create_index('ix_stock_ledger_product', 'stock_ledger', ['product_id'], unique=False)
    op.create_index('ix_stock_ledger_location', 'stock_ledger', ['location_id'], unique=False)
    op.create_index('ix_stock_ledger_warehouse_id', 'stock_ledger', ['warehouse_id'], unique=False)
    op.create_index('ix_stock_ledger_operation_type', 'stock_ledger', ['operation_type'], unique=False)
    op.create_index('ix_stock_ledger_created_at', 'stock_ledger', ['created_at'], unique=False)
    op.create_index('ix_stock_ledger_ref', 'stock_ledger', ['reference_type', 'reference_id'], unique=False)

    # 12. receipts
    op.create_table(
        'receipts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_number', sa.String(length=100), nullable=False),
        sa.Column('supplier_id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('destination_location_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('validated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['destination_location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['validated_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_receipts_id', 'receipts', ['id'], unique=False)
    op.create_index('ix_receipts_receipt_number', 'receipts', ['receipt_number'], unique=True)
    op.create_index('ix_receipts_status', 'receipts', ['status'], unique=False)
    op.create_index('ix_receipts_supplier_id', 'receipts', ['supplier_id'], unique=False)
    op.create_index('ix_receipts_warehouse_id', 'receipts', ['warehouse_id'], unique=False)

    # 13. receipt_items
    op.create_table(
        'receipt_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('uom_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uom_id'], ['uoms.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_receipt_items_id', 'receipt_items', ['id'], unique=False)
    op.create_index('ix_receipt_items_product_id', 'receipt_items', ['product_id'], unique=False)
    op.create_index('ix_receipt_items_receipt_id', 'receipt_items', ['receipt_id'], unique=False)

    # 14. deliveries
    op.create_table(
        'deliveries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('delivery_number', sa.String(length=100), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('source_location_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('validated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['source_location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['validated_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_deliveries_delivery_number', 'deliveries', ['delivery_number'], unique=True)
    op.create_index('ix_deliveries_id', 'deliveries', ['id'], unique=False)
    op.create_index('ix_deliveries_status', 'deliveries', ['status'], unique=False)
    op.create_index('ix_deliveries_customer_id', 'deliveries', ['customer_id'], unique=False)
    op.create_index('ix_deliveries_warehouse_id', 'deliveries', ['warehouse_id'], unique=False)

    # 15. delivery_items
    op.create_table(
        'delivery_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('delivery_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('uom_id', sa.Integer(), nullable=False),
        sa.Column('picked_quantity', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('packed_quantity', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['delivery_id'], ['deliveries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['uom_id'], ['uoms.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_delivery_items_delivery_id', 'delivery_items', ['delivery_id'], unique=False)
    op.create_index('ix_delivery_items_id', 'delivery_items', ['id'], unique=False)
    op.create_index('ix_delivery_items_product_id', 'delivery_items', ['product_id'], unique=False)

    # 16. transfers
    op.create_table(
        'transfers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transfer_number', sa.String(length=100), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('source_location_id', sa.Integer(), nullable=False),
        sa.Column('destination_location_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('validated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['destination_location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['source_location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['validated_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_transfers_id', 'transfers', ['id'], unique=False)
    op.create_index('ix_transfers_status', 'transfers', ['status'], unique=False)
    op.create_index('ix_transfers_transfer_number', 'transfers', ['transfer_number'], unique=True)
    op.create_index('ix_transfers_warehouse_id', 'transfers', ['warehouse_id'], unique=False)

    # 17. transfer_items
    op.create_table(
        'transfer_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transfer_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('uom_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['transfer_id'], ['transfers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uom_id'], ['uoms.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_transfer_items_id', 'transfer_items', ['id'], unique=False)
    op.create_index('ix_transfer_items_product_id', 'transfer_items', ['product_id'], unique=False)
    op.create_index('ix_transfer_items_transfer_id', 'transfer_items', ['transfer_id'], unique=False)

    # 18. adjustments
    op.create_table(
        'adjustments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('adjustment_number', sa.String(length=100), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='DRAFT'),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('validated_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['validated_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_adjustments_adjustment_number', 'adjustments', ['adjustment_number'], unique=True)
    op.create_index('ix_adjustments_id', 'adjustments', ['id'], unique=False)
    op.create_index('ix_adjustments_status', 'adjustments', ['status'], unique=False)
    op.create_index('ix_adjustments_warehouse_id', 'adjustments', ['warehouse_id'], unique=False)

    # 19. adjustment_items
    op.create_table(
        'adjustment_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('adjustment_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('system_quantity', sa.Float(), nullable=False),
        sa.Column('counted_quantity', sa.Float(), nullable=False),
        sa.Column('difference', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['adjustment_id'], ['adjustments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_adjustment_items_adjustment_id', 'adjustment_items', ['adjustment_id'], unique=False)
    op.create_index('ix_adjustment_items_id', 'adjustment_items', ['id'], unique=False)
    op.create_index('ix_adjustment_items_product_id', 'adjustment_items', ['product_id'], unique=False)

    # 20. reorder_rules
    op.create_table(
        'reorder_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('minimum_quantity', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('maximum_quantity', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reorder_rules_id', 'reorder_rules', ['id'], unique=False)
    op.create_index('ix_reorder_rules_location_id', 'reorder_rules', ['location_id'], unique=False)
    op.create_index('ix_reorder_rules_product_id', 'reorder_rules', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_table('reorder_rules')
    op.drop_table('adjustment_items')
    op.drop_table('adjustments')
    op.drop_table('transfer_items')
    op.drop_table('transfers')
    op.drop_table('delivery_items')
    op.drop_table('deliveries')
    op.drop_table('receipt_items')
    op.drop_table('receipts')
    op.drop_table('stock_ledger')
    op.drop_table('stock_balances')
    op.drop_table('customers')
    op.drop_table('suppliers')
    op.drop_table('locations')
    op.drop_table('warehouses')
    op.drop_table('products')
    op.drop_table('uoms')
    op.drop_table('categories')
    op.drop_table('password_reset_otps')
    op.drop_table('users')
