import { useEffect, useState } from 'react'
import { apiError, authApi, masterApi, stockApi } from '../services/api'
import type { LedgerEntry, StockSummary, User, Warehouse } from '../types'


export function StockPage() {
  const [rows, setRows] = useState<StockSummary[]>([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    setError('')
    stockApi
      .summary(search || undefined)
      .then(setRows)
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const exportCSV = () => {
    if (!rows.length) return
    const headers = ['SKU', 'Product Name', 'Category', 'Unit', 'On Hand', 'Reserved', 'Free to Use', 'Reorder Level', 'Status']
    const csvRows = rows.map((r) => [
      `"${r.product_sku}"`,
      `"${r.product_name}"`,
      `"${r.category_name || ''}"`,
      `"${r.uom_code || ''}"`,
      r.on_hand ?? r.total_quantity,
      r.reserved ?? 0,
      r.free_to_use ?? r.total_quantity,
      r.reorder_level,
      r.total_quantity <= 0 ? 'OUT OF STOCK' : r.is_low_stock ? 'LOW STOCK' : 'NORMAL',
    ])
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...csvRows.map((e) => e.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', `stocksense_inventory_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Current stock</h1>
          <p>Live inventory balances calculated from backend ledger (Free to Use = On Hand − Reserved).</p>
        </div>
        <div className="row-actions">
          <button className="btn secondary" onClick={exportCSV} disabled={rows.length === 0}>
            Export CSV
          </button>
        </div>
      </div>
      <div className="toolbar">
        <input
          placeholder="Filter by SKU or name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && load()}
        />
        <button className="btn secondary" onClick={load}>
          Search
        </button>
        {search && (
          <button
            className="btn secondary"
            onClick={() => {
              setSearch('')
              stockApi.summary().then(setRows).catch((err) => setError(apiError(err)))
            }}
          >
            Clear
          </button>
        )}
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {loading ? (
          <p className="muted">Loading stock balances…</p>
        ) : rows.length === 0 ? (
          <p className="empty">No stock records found.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Product</th>
                <th>Category</th>
                <th>On Hand</th>
                <th>Reserved</th>
                <th>Free to Use</th>
                <th>Reorder Level</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const onHand = r.on_hand ?? r.total_quantity
                const reserved = r.reserved ?? 0
                const freeToUse = r.free_to_use ?? Math.max(0, onHand - reserved)
                const isOut = onHand <= 0
                const isLow = r.is_low_stock || onHand <= r.reorder_level
                return (
                  <tr key={r.product_id}>
                    <td>
                      <strong>{r.product_sku}</strong>
                    </td>
                    <td>{r.product_name}</td>
                    <td className="muted">{r.category_name || '—'}</td>
                    <td>
                      {onHand} <span className="muted">{r.uom_code}</span>
                    </td>
                    <td>
                      {reserved} <span className="muted">{r.uom_code}</span>
                    </td>
                    <td>
                      <strong>{freeToUse}</strong> <span className="muted">{r.uom_code}</span>
                    </td>
                    <td>{r.reorder_level}</td>
                    <td>
                      <span className={`badge ${isOut ? 'OUT_OF_STOCK' : isLow ? 'LOW_STOCK' : 'NORMAL'}`}>
                        {isOut ? 'OUT OF STOCK' : isLow ? 'LOW STOCK' : 'NORMAL'}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}


export function LedgerPage() {
  const [rows, setRows] = useState<LedgerEntry[]>([])
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [operation, setOperation] = useState('')
  const [warehouseId, setWarehouseId] = useState('')
  const [searchRef, setSearchRef] = useState('')
  const [viewMode, setViewMode] = useState<'list' | 'kanban'>('list')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    setError('')
    stockApi
      .ledger({
        operation_type: operation || undefined,
        warehouse_id: warehouseId ? Number(warehouseId) : undefined,
      })
      .then((data) => {
        let filtered = data
        if (searchRef.trim()) {
          const s = searchRef.toLowerCase()
          filtered = filtered.filter(
            (e) =>
              e.reference_id.toLowerCase().includes(s) ||
              e.product_name.toLowerCase().includes(s) ||
              e.product_sku.toLowerCase().includes(s) ||
              (e.created_by_name && e.created_by_name.toLowerCase().includes(s)),
          )
        }
        setRows(filtered)
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    masterApi.warehouses().then(setWarehouses).catch((err) => setError(apiError(err)))
    load()
  }, [])

  const exportCSV = () => {
    if (!rows.length) return
    const headers = ['Timestamp', 'Product SKU', 'Product Name', 'Warehouse', 'Location', 'Operation', 'Reference', 'Before', 'Change', 'After', 'User']
    const csvRows = rows.map((e) => [
      `"${new Date(e.created_at).toISOString()}"`,
      `"${e.product_sku}"`,
      `"${e.product_name}"`,
      `"${e.warehouse_name}"`,
      `"${e.location_name}"`,
      `"${e.operation_type}"`,
      `"${e.reference_id}"`,
      e.quantity_before,
      e.quantity_change,
      e.quantity_after,
      `"${e.created_by_name || ''}"`,
    ])
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...csvRows.map((r) => r.join(','))].join('\n')
    const encodedUri = encodeURI(csvContent)
    const link = document.createElement('a')
    link.setAttribute('href', encodedUri)
    link.setAttribute('download', `stocksense_move_history_${new Date().toISOString().slice(0, 10)}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Move history</h1>
          <p>Append-only stock movements ledger. Every receipt, delivery, transfer, and adjustment is recorded here.</p>
        </div>
        <div className="row-actions">
          <button
            className={`btn ${viewMode === 'list' ? '' : 'secondary'}`}
            onClick={() => setViewMode('list')}
          >
            List View
          </button>
          <button
            className={`btn ${viewMode === 'kanban' ? '' : 'secondary'}`}
            onClick={() => setViewMode('kanban')}
          >
            Kanban View
          </button>
          <button className="btn secondary" onClick={exportCSV} disabled={rows.length === 0}>
            Export CSV
          </button>
        </div>
      </div>
      <div className="toolbar">
        <input
          placeholder="Filter by Ref, Product, SKU or User…"
          value={searchRef}
          onChange={(e) => setSearchRef(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && load()}
        />
        <select value={operation} onChange={(e) => setOperation(e.target.value)}>
          <option value="">All operations</option>
          {['INITIAL', 'RECEIPT', 'DELIVERY', 'TRANSFER_OUT', 'TRANSFER_IN', 'ADJUSTMENT'].map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>
        <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)}>
          <option value="">All warehouses</option>
          {warehouses.map((w) => (
            <option key={w.id} value={w.id}>
              {w.name}
            </option>
          ))}
        </select>
        <button className="btn secondary" onClick={load}>
          Filter
        </button>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      
      {loading ? (
        <p className="muted">Loading move history…</p>
      ) : rows.length === 0 ? (
        <div className="panel">
          <p className="empty">No move history records match the filters.</p>
        </div>
      ) : viewMode === 'list' ? (
        <div className="panel">
          <table>
            <thead>
              <tr>
                <th>Date & Time</th>
                <th>Product</th>
                <th>Location</th>
                <th>Operation</th>
                <th>Reference</th>
                <th>Before</th>
                <th>Change</th>
                <th>After</th>
                <th>Responsible</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((e) => (
                <tr key={e.id}>
                  <td>{new Date(e.created_at).toLocaleString()}</td>
                  <td>
                    <strong>{e.product_name}</strong>
                    <div className="muted">{e.product_sku}</div>
                  </td>
                  <td>
                    {e.warehouse_name} / {e.location_name}
                  </td>
                  <td>
                    <span className="badge DRAFT">{e.operation_type}</span>
                  </td>
                  <td>
                    <code>{e.reference_id}</code>
                  </td>
                  <td>{e.quantity_before}</td>
                  <td>
                    <strong style={{ color: e.quantity_change > 0 ? 'var(--ok)' : 'var(--danger)' }}>
                      {e.quantity_change > 0 ? '+' : ''}
                      {e.quantity_change}
                    </strong>
                  </td>
                  <td>{e.quantity_after}</td>
                  <td>{e.created_by_name || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="kpis" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
          {['RECEIPT', 'DELIVERY', 'TRANSFER_OUT', 'TRANSFER_IN', 'ADJUSTMENT', 'INITIAL'].map((opType) => {
            const items = rows.filter((r) => r.operation_type === opType)
            return (
              <div key={opType} className="panel" style={{ minHeight: 220 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                  <span className="badge DRAFT">{opType}</span>
                  <span className="muted">{items.length} moves</span>
                </div>
                {items.length === 0 ? (
                  <p className="empty" style={{ fontSize: 13 }}>No movements in this category.</p>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {items.slice(0, 10).map((m) => (
                      <div key={m.id} className="meta-box" style={{ padding: 10 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <strong>{m.product_name}</strong>
                          <strong style={{ color: m.quantity_change > 0 ? 'var(--ok)' : 'var(--danger)' }}>
                            {m.quantity_change > 0 ? '+' : ''}
                            {m.quantity_change}
                          </strong>
                        </div>
                        <div className="muted" style={{ fontSize: 12 }}>
                          {m.reference_id} · {m.location_name}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </>
  )
}


export function WarehousesPage() {
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [name, setName] = useState('')
  const [code, setCode] = useState('')
  const [address, setAddress] = useState('')
  const [locWh, setLocWh] = useState('')
  const [locName, setLocName] = useState('')
  const [locCode, setLocCode] = useState('')
  const [error, setError] = useState('')
  const [locations, setLocations] = useState<{ id: number; name: string; code: string; warehouse_name?: string | null }[]>([])

  const load = () => {
    masterApi.warehouses().then(setWarehouses).catch((err) => setError(apiError(err)))
    masterApi.locations().then(setLocations).catch((err) => setError(apiError(err)))
  }
  useEffect(load, [])

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Warehouse settings</h1>
          <p>Locations belong to a warehouse. Inactive warehouses should not take new operations.</p>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="grid-2">
        <div className="panel">
          <h3>Warehouses</h3>
          <form
            className="form"
            onSubmit={async (e) => {
              e.preventDefault()
              try {
                await masterApi.createWarehouse({ name, code, address })
                setName('')
                setCode('')
                setAddress('')
                load()
              } catch (err) {
                setError(apiError(err))
              }
            }}
          >
            <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
            <input placeholder="Code" value={code} onChange={(e) => setCode(e.target.value)} required />
            <input placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} />
            <button className="btn">Add warehouse</button>
          </form>
          <table>
            <thead>
              <tr>
                <th>Code</th>
                <th>Name</th>
              </tr>
            </thead>
            <tbody>
              {warehouses.map((w) => (
                <tr key={w.id}>
                  <td>{w.code}</td>
                  <td>{w.name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="panel">
          <h3>Locations</h3>
          <form
            className="form"
            onSubmit={async (e) => {
              e.preventDefault()
              try {
                await masterApi.createLocation({
                  warehouse_id: Number(locWh),
                  name: locName,
                  code: locCode,
                  location_type: 'STORAGE',
                })
                setLocName('')
                setLocCode('')
                load()
              } catch (err) {
                setError(apiError(err))
              }
            }}
          >
            <select value={locWh} onChange={(e) => setLocWh(e.target.value)} required>
              <option value="">Warehouse</option>
              {warehouses.map((w) => (
                <option key={w.id} value={w.id}>
                  {w.name}
                </option>
              ))}
            </select>
            <input placeholder="Location name" value={locName} onChange={(e) => setLocName(e.target.value)} required />
            <input placeholder="Code" value={locCode} onChange={(e) => setLocCode(e.target.value)} required />
            <button className="btn">Add location</button>
          </form>
          <table>
            <thead>
              <tr>
                <th>Warehouse</th>
                <th>Location</th>
                <th>Code</th>
              </tr>
            </thead>
            <tbody>
              {locations.map((l) => (
                <tr key={l.id}>
                  <td>{l.warehouse_name}</td>
                  <td>{l.name}</td>
                  <td>{l.code}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

export function ProfilePage() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    authApi
      .me()
      .then((data) => {
        setUser(data)
        localStorage.setItem('ss_user', JSON.stringify(data))
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div style={{ maxWidth: 840 }}>
      <div className="page-head">
        <div>
          <h1>My Profile</h1>
          <p>Live verified account credentials from StockSense authentication service.</p>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      {loading ? (
        <p className="muted">Fetching verified profile…</p>
      ) : user ? (
        <div className="panel">
          <div className="detail-meta" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16 }}>
            <div className="meta-box">
              <span>Full Name</span>
              <strong style={{ fontSize: 16, color: 'var(--text-main)' }}>{user.full_name}</strong>
            </div>
            <div className="meta-box">
              <span>Email Address</span>
              <strong style={{ fontSize: 16, color: 'var(--text-main)' }}>{user.email}</strong>
            </div>
            <div className="meta-box">
              <span>Assigned Role</span>
              <div style={{ marginTop: 4 }}>
                <span className={`badge ${user.role === 'INVENTORY_MANAGER' ? 'READY' : 'DONE'}`}>
                  {user.role.replaceAll('_', ' ')}
                </span>
              </div>
            </div>
            <div className="meta-box">
              <span>Account Status</span>
              <div style={{ marginTop: 4 }}>
                <span className="badge NORMAL">ACTIVE</span>
              </div>
            </div>
          </div>
          <div style={{ marginTop: 20, paddingTop: 16, borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="muted" style={{ fontSize: 13 }}>
              Member since: {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'Active Session'}
            </span>
          </div>
        </div>
      ) : (
        <div className="panel">
          <p className="empty">No profile data available.</p>
        </div>
      )}
    </div>
  )
}

