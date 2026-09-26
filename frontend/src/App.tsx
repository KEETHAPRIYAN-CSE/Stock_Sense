import type { ReactNode } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { useAuth } from './context/AuthContext'
import { ForgotPasswordPage, LoginPage, RegisterPage, ResetPasswordPage } from './pages/AuthPages'
import DashboardPage from './pages/DashboardPage'
import {
  AdjustmentCreatePage,
  AdjustmentDetailPage,
  AdjustmentsPage,
  DeliveriesPage,
  DeliveryCreatePage,
  DeliveryDetailPage,
  ReceiptCreatePage,
  ReceiptDetailPage,
  ReceiptsPage,
  TransferCreatePage,
  TransferDetailPage,
  TransfersPage,
} from './pages/OperationsPages'
import { ProductDetailPage, ProductFormPage, ProductsPage } from './pages/ProductsPages'
import { LedgerPage, ProfilePage, StockPage, WarehousesPage } from './pages/StockPages'

function Protected({ children }: { children: ReactNode }) {
  const { token } = useAuth()
  if (!token) return <Navigate to="/login" replace />
  return children
}

function Guest({ children }: { children: ReactNode }) {
  const { token } = useAuth()
  if (token) return <Navigate to="/" replace />
  return children
}

export default function App() {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <Guest>
            <LoginPage />
          </Guest>
        }
      />
      <Route
        path="/register"
        element={
          <Guest>
            <RegisterPage />
          </Guest>
        }
      />
      <Route
        path="/forgot-password"
        element={
          <Guest>
            <ForgotPasswordPage />
          </Guest>
        }
      />
      <Route
        path="/reset-password"
        element={
          <Guest>
            <ResetPasswordPage />
          </Guest>
        }
      />
      <Route
        element={
          <Protected>
            <Layout />
          </Protected>
        }
      >
        <Route path="/" element={<DashboardPage />} />
        <Route path="/stock" element={<StockPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/products/new" element={<ProductFormPage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="/receipts" element={<ReceiptsPage />} />
        <Route path="/receipts/new" element={<ReceiptCreatePage />} />
        <Route path="/receipts/:id" element={<ReceiptDetailPage />} />
        <Route path="/deliveries" element={<DeliveriesPage />} />
        <Route path="/deliveries/new" element={<DeliveryCreatePage />} />
        <Route path="/deliveries/:id" element={<DeliveryDetailPage />} />
        <Route path="/transfers" element={<TransfersPage />} />
        <Route path="/transfers/new" element={<TransferCreatePage />} />
        <Route path="/transfers/:id" element={<TransferDetailPage />} />
        <Route path="/adjustments" element={<AdjustmentsPage />} />
        <Route path="/adjustments/new" element={<AdjustmentCreatePage />} />
        <Route path="/adjustments/:id" element={<AdjustmentDetailPage />} />
        <Route path="/ledger" element={<LedgerPage />} />
        <Route path="/warehouses" element={<WarehousesPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
