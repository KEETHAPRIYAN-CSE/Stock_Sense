import axios, { type AxiosError } from 'axios'
import type {
  Adjustment,
  DashboardSummary,
  Delivery,
  LedgerEntry,
  Location,
  LowStockProduct,
  Product,
  Receipt,
  RecentMovement,
  StockSummary,
  TokenResponse,
  Transfer,
  User,
  Warehouse,
} from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('ss_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function apiError(err: unknown): string {
  const ax = err as AxiosError<{ detail?: unknown }>
  const detail = ax.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (item && typeof item === 'object' && 'msg' in item) return String((item as { msg: string }).msg)
        return JSON.stringify(item)
      })
      .join('; ')
  }
  return ax.message || 'Request failed'
}

export const authApi = {
  login: (email: string, password: string) =>
    api.post<TokenResponse>('/api/auth/login', { email, password }).then((r) => r.data),
  register: (payload: { email: string; password: string; full_name: string; role: string }) =>
    api.post<TokenResponse>('/api/auth/register', payload).then((r) => r.data),
  me: () => api.get<User>('/api/auth/me').then((r) => r.data),
  logout: () => api.post('/api/auth/logout').then((r) => r.data),
  forgot: (email: string) =>
    api.post<{ message: string; dev_otp?: string | null }>('/api/auth/forgot-password', { email }).then((r) => r.data),
  reset: (email: string, otp: string, new_password: string) =>
    api.post('/api/auth/reset-password', { email, otp, new_password }).then((r) => r.data),
}

export const masterApi = {
  products: (params?: { search?: string; category_id?: number }) =>
    api.get<Product[]>('/api/products', { params }).then((r) => r.data),
  product: (id: number) => api.get<Product>(`/api/products/${id}`).then((r) => r.data),
  createProduct: (payload: Record<string, unknown>) =>
    api.post<Product>('/api/products', payload).then((r) => r.data),
  updateProduct: (id: number, payload: Record<string, unknown>) =>
    api.put<Product>(`/api/products/${id}`, payload).then((r) => r.data),
  categories: () => api.get<Named[]>('/api/categories').then((r) => r.data),
  createCategory: (name: string) => api.post('/api/categories', { name }).then((r) => r.data),
  uoms: () => api.get<Named[]>('/api/uoms').then((r) => r.data),
  warehouses: () => api.get<Warehouse[]>('/api/warehouses').then((r) => r.data),
  createWarehouse: (payload: { name: string; code: string; address?: string }) =>
    api.post<Warehouse>('/api/warehouses', payload).then((r) => r.data),
  locations: (warehouse_id?: number) =>
    api.get<Location[]>('/api/locations', { params: warehouse_id ? { warehouse_id } : {} }).then((r) => r.data),
  createLocation: (payload: { warehouse_id: number; name: string; code: string; location_type: string }) =>
    api.post<Location>('/api/locations', payload).then((r) => r.data),
  suppliers: () => api.get<Named[]>('/api/suppliers').then((r) => r.data),
  customers: () => api.get<Named[]>('/api/customers').then((r) => r.data),
}

type Named = { id: number; name: string; code?: string }

export const dashboardApi = {
  summary: () => api.get<DashboardSummary>('/api/dashboard/summary').then((r) => r.data),
  lowStock: () => api.get<LowStockProduct[]>('/api/dashboard/low-stock').then((r) => r.data),
  movements: () => api.get<RecentMovement[]>('/api/dashboard/recent-movements').then((r) => r.data),
}

export const stockApi = {
  summary: (search?: string) =>
    api.get<StockSummary[]>('/api/stock', { params: search ? { search } : {} }).then((r) => r.data),
  locations: (productId: number) =>
    api.get(`/api/stock/${productId}/locations`).then((r) => r.data),
  ledger: (params?: Record<string, string | number | undefined>) =>
    api.get<LedgerEntry[]>('/api/stock/ledger', { params }).then((r) => r.data),
}

export const opsApi = {
  receipts: () => api.get<Receipt[]>('/api/receipts').then((r) => r.data),
  receipt: (id: number) => api.get<Receipt>(`/api/receipts/${id}`).then((r) => r.data),
  createReceipt: (payload: Record<string, unknown>) => api.post<Receipt>('/api/receipts', payload).then((r) => r.data),
  validateReceipt: (id: number) => api.post<Receipt>(`/api/receipts/${id}/validate`).then((r) => r.data),
  cancelReceipt: (id: number) => api.post<Receipt>(`/api/receipts/${id}/cancel`).then((r) => r.data),

  deliveries: () => api.get<Delivery[]>('/api/deliveries').then((r) => r.data),
  delivery: (id: number) => api.get<Delivery>(`/api/deliveries/${id}`).then((r) => r.data),
  createDelivery: (payload: Record<string, unknown>) => api.post<Delivery>('/api/deliveries', payload).then((r) => r.data),
  pickDelivery: (id: number) => api.post<Delivery>(`/api/deliveries/${id}/pick`).then((r) => r.data),
  packDelivery: (id: number) => api.post<Delivery>(`/api/deliveries/${id}/pack`).then((r) => r.data),
  validateDelivery: (id: number) => api.post<Delivery>(`/api/deliveries/${id}/validate`).then((r) => r.data),
  cancelDelivery: (id: number) => api.post<Delivery>(`/api/deliveries/${id}/cancel`).then((r) => r.data),

  transfers: () => api.get<Transfer[]>('/api/transfers').then((r) => r.data),
  transfer: (id: number) => api.get<Transfer>(`/api/transfers/${id}`).then((r) => r.data),
  createTransfer: (payload: Record<string, unknown>) => api.post<Transfer>('/api/transfers', payload).then((r) => r.data),
  validateTransfer: (id: number) => api.post<Transfer>(`/api/transfers/${id}/validate`).then((r) => r.data),
  cancelTransfer: (id: number) => api.post<Transfer>(`/api/transfers/${id}/cancel`).then((r) => r.data),

  adjustments: () => api.get<Adjustment[]>('/api/adjustments').then((r) => r.data),
  adjustment: (id: number) => api.get<Adjustment>(`/api/adjustments/${id}`).then((r) => r.data),
  createAdjustment: (payload: Record<string, unknown>) =>
    api.post<Adjustment>('/api/adjustments', payload).then((r) => r.data),
  validateAdjustment: (id: number) => api.post<Adjustment>(`/api/adjustments/${id}/validate`).then((r) => r.data),
  cancelAdjustment: (id: number) => api.post<Adjustment>(`/api/adjustments/${id}/cancel`).then((r) => r.data),
}
