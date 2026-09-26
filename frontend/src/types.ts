export type User = {
  id: number
  email: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
  last_login_at?: string | null
}

export type TokenResponse = {
  access_token: string
  token_type: string
  user: User
}

export type Product = {
  id: number
  name: string
  sku: string
  category_id?: number | null
  uom_id: number
  initial_stock: number
  reorder_level: number
  is_active: boolean
  category_name?: string | null
  uom_code?: string | null
  uom_name?: string | null
  total_stock: number
  location_stocks?: { location_id: number; location_name: string; warehouse_name: string; quantity: number }[]
}

export type NamedId = { id: number; name: string; code?: string; warehouse_id?: number; warehouse_name?: string | null }

export type DashboardSummary = {
  total_products: number
  low_stock_count: number
  out_of_stock_count: number
  pending_receipts: number
  pending_deliveries: number
  scheduled_transfers: number
  total_warehouses: number
}

export type LowStockProduct = {
  product_id: number
  product_name: string
  product_sku: string
  category_name?: string | null
  current_stock: number
  reorder_level: number
  uom_code?: string | null
}

export type RecentMovement = {
  id: number
  date: string
  product_name: string
  product_sku: string
  warehouse_name: string
  location_name: string
  operation_type: string
  reference_id: string
  quantity_change: number
  quantity_after: number
}

export type StockSummary = {
  product_id: number
  product_name: string
  product_sku: string
  category_name?: string | null
  uom_code?: string | null
  total_quantity: number
  reorder_level: number
  is_low_stock: boolean
}

export type LedgerEntry = {
  id: number
  product_id: number
  product_name: string
  product_sku: string
  warehouse_name: string
  location_name: string
  operation_type: string
  reference_type: string
  reference_id: string
  quantity_before: number
  quantity_change: number
  quantity_after: number
  created_by_name?: string | null
  created_at: string
  notes?: string | null
}

export type LineItem = {
  id: number
  product_id: number
  product_name: string
  product_sku: string
  quantity: number
  uom_id: number
  uom_code: string
  picked_quantity?: number
  packed_quantity?: number
  system_quantity?: number
  counted_quantity?: number
  difference?: number
}

export type Receipt = {
  id: number
  receipt_number: string
  supplier_id: number
  supplier_name: string
  warehouse_id: number
  warehouse_name: string
  destination_location_id: number
  destination_location_name: string
  status: string
  scheduled_at?: string | null
  created_by_name?: string | null
  created_at: string
  validated_at?: string | null
  total_items: number
  total_quantity: number
  items?: LineItem[]
}

export type Delivery = {
  id: number
  delivery_number: string
  customer_id: number
  customer_name: string
  warehouse_id: number
  warehouse_name: string
  source_location_id: number
  source_location_name: string
  status: string
  created_by_name?: string | null
  created_at: string
  validated_at?: string | null
  total_items: number
  total_quantity: number
  items?: LineItem[]
}

export type Transfer = {
  id: number
  transfer_number: string
  warehouse_id: number
  warehouse_name: string
  source_location_id: number
  source_location_name: string
  destination_location_id: number
  destination_location_name: string
  status: string
  created_by_name?: string | null
  created_at: string
  validated_at?: string | null
  total_items: number
  total_quantity: number
  items?: LineItem[]
}

export type Adjustment = {
  id: number
  adjustment_number: string
  warehouse_id: number
  warehouse_name: string
  location_id: number
  location_name: string
  status: string
  reason?: string | null
  created_by_name?: string | null
  created_at: string
  validated_at?: string | null
  total_items: number
  items?: LineItem[]
}

export type Warehouse = {
  id: number
  name: string
  code: string
  address?: string | null
  is_active: boolean
}

export type Location = {
  id: number
  warehouse_id: number
  name: string
  code: string
  location_type: string
  is_active: boolean
  warehouse_name?: string | null
}
