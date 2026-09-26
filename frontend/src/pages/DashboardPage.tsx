import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AlertTriangle, ArrowUpRight, Boxes, CheckCircle2, ClipboardList, Layers, Package, TrendingDown, TrendingUp, Truck, Warehouse } from 'lucide-react'
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
          <h1>Inventory Dashboard</h1>
          <p>Real-time operational ledger metrics & stock replenishment intelligence.</p>
        </div>
        <div className="row-actions">
          <Link className="btn secondary" to="/stock">
            <Boxes size={16} /> View Stock
          </Link>
          <Link className="btn" to="/receipts/new">
            <ClipboardList size={16} /> Receive Stock
          </Link>
        </div>
      </div>
      <div className="kpis">
        <div className="kpi">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Total Products</span>
            <Package size={20} color="var(--accent-light)" />
          </div>
          <strong>{summary.total_products}</strong>
        </div>
        <div className="kpi" style={{ borderColor: summary.low_stock_count > 0 ? 'rgba(245, 158, 11, 0.3)' : undefined }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Low / Out Of Stock</span>
            <AlertTriangle size={20} color={summary.low_stock_count > 0 ? 'var(--warn)' : 'var(--text-dim)'} />
          </div>
          <strong>
            {summary.low_stock_count} <span style={{ fontSize: 16, color: 'var(--text-dim)', fontWeight: 600 }}>/ {summary.out_of_stock_count}</span>
          </strong>
        </div>
        <div className="kpi">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Pending Receipts</span>
            <ClipboardList size={20} color="var(--info)" />
          </div>
          <strong>{summary.pending_receipts}</strong>
        </div>
        <div className="kpi">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Pending Deliveries</span>
            <Truck size={20} color="var(--ok)" />
          </div>
          <strong>{summary.pending_deliveries}</strong>
        </div>
        <div className="kpi">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Transfers</span>
            <Layers size={20} color="var(--accent-light)" />
          </div>
          <strong>{summary.scheduled_transfers}</strong>
        </div>
        <div className="kpi">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Warehouses</span>
            <Warehouse size={20} color="var(--text-muted)" />
          </div>
          <strong>{summary.total_warehouses}</strong>
        </div>
      </div>
      <div className="grid-2">
        <div className="panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
            <h3>Recent Movements</h3>
            <Link to="/ledger" style={{ fontSize: 13, color: 'var(--accent-light)', display: 'inline-flex', alignItems: 'center', gap: 4, fontWeight: 600 }}>
              Full History <ArrowUpRight size={14} />
            </Link>
          </div>
          {moves.length === 0 ? (
            <p className="empty">No ledger activity yet. Validate a receipt to start the trail.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Product</th>
                  <th>Type</th>
                  <th>Quantity</th>
                </tr>
              </thead>
              <tbody>
                {moves.map((m) => (
                  <tr key={m.id}>
                    <td>{m.date}</td>
                    <td>
                      <strong>{m.product_name}</strong>
                      <div className="muted">{m.reference_id}</div>
                    </td>
                    <td>
                      <span className="badge DRAFT">{m.operation_type}</span>
                    </td>
                    <td>
                      <strong style={{ color: m.quantity_change > 0 ? 'var(--ok)' : 'var(--danger)', display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                        {m.quantity_change > 0 ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                        {m.quantity_change > 0 ? '+' : ''}
                        {m.quantity_change}
                      </strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <div className="panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
            <h3>Low Stock Watchlist</h3>
            <Link to="/stock" style={{ fontSize: 13, color: 'var(--accent-light)', display: 'inline-flex', alignItems: 'center', gap: 4, fontWeight: 600 }}>
              All Balances <ArrowUpRight size={14} />
            </Link>
          </div>
          {low.length === 0 ? (
            <div style={{ padding: '24px 12px', textAlign: 'center' }}>
              <CheckCircle2 size={32} color="var(--ok)" style={{ margin: '0 auto 12px' }} />
              <p className="empty">All inventory levels are healthy above reorder thresholds.</p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Current</th>
                  <th>Reorder Level</th>
                </tr>
              </thead>
              <tbody>
                {low.map((p) => (
                  <tr key={p.product_id}>
                    <td>
                      <strong>{p.product_name}</strong>
                      <div className="muted">{p.product_sku}</div>
                    </td>
                    <td>
                      <span className="badge OUT_OF_STOCK">{p.current_stock}</span>
                    </td>
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

