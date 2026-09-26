import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiError, dashboardApi } from '../services/api'
import type { DashboardSummary, LowStockProduct, RecentMovement } from '../types'

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [low, setLow] = useState<LowStockProduct[]>([])
  const [moves, setMoves] = useState<RecentMovement[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([dashboardApi.summary(), dashboardApi.lowStock(), dashboardApi.movements()])
      .then(([s, l, m]) => {
        setSummary(s)
        setLow(l)
        setMoves(m)
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="muted">Loading dashboard…</p>
  if (error) return <div className="alert">{error}</div>
  if (!summary) return <p className="empty">No dashboard data.</p>

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Inventory dashboard</h1>
          <p>Live counts from PostgreSQL — not a static snapshot.</p>
        </div>
        <Link className="btn" to="/receipts/new">
          Receive stock
        </Link>
      </div>
      <div className="kpis">
        <div className="kpi">
          <span>Total products</span>
          <strong>{summary.total_products}</strong>
        </div>
        <div className="kpi">
          <span>Low / out of stock</span>
          <strong>
            {summary.low_stock_count} / {summary.out_of_stock_count}
          </strong>
        </div>
        <div className="kpi">
          <span>Pending receipts</span>
          <strong>{summary.pending_receipts}</strong>
        </div>
        <div className="kpi">
          <span>Pending deliveries</span>
          <strong>{summary.pending_deliveries}</strong>
        </div>
        <div className="kpi">
          <span>Scheduled transfers</span>
          <strong>{summary.scheduled_transfers}</strong>
        </div>
        <div className="kpi">
          <span>Warehouses</span>
          <strong>{summary.total_warehouses}</strong>
        </div>
      </div>
      <div className="grid-2">
        <div className="panel">
          <h3>Recent movements</h3>
          {moves.length === 0 ? (
            <p className="empty">No ledger activity yet. Validate a receipt to start the trail.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Product</th>
                  <th>Type</th>
                  <th>Change</th>
                </tr>
              </thead>
              <tbody>
                {moves.map((m) => (
                  <tr key={m.id}>
                    <td>{m.date}</td>
                    <td>
                      {m.product_name}
                      <div className="muted">{m.reference_id}</div>
                    </td>
                    <td>{m.operation_type}</td>
                    <td>
                      {m.quantity_change > 0 ? '+' : ''}
                      {m.quantity_change}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <div className="panel">
          <h3>Low stock</h3>
          {low.length === 0 ? (
            <p className="empty">No products are at or below reorder level.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Qty</th>
                  <th>Reorder</th>
                </tr>
              </thead>
              <tbody>
                {low.map((p) => (
                  <tr key={p.product_id}>
                    <td>
                      {p.product_name}
                      <div className="muted">{p.product_sku}</div>
                    </td>
                    <td>{p.current_stock}</td>
                    <td>{p.reorder_level}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </>
  )
}
