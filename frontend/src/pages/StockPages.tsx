import { useEffect, useState } from 'react'
import { apiError, masterApi, stockApi } from '../services/api'
import type { LedgerEntry, StockSummary, Warehouse } from '../types'

export function StockPage() {
  const [rows, setRows] = useState<StockSummary[]>([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')

  const load = () => {
    stockApi
      .summary(search || undefined)
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }

  useEffect(load, [])

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Current stock</h1>
          <p>Aggregated from stock_balances. Low-stock uses each product reorder level.</p>
        </div>
      </div>
      <div className="toolbar">
        <input placeholder="SKU or name" value={search} onChange={(e) => setSearch(e.target.value)} />
        <button className="btn secondary" onClick={load}>
          Search
        </button>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No stock rows yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Product</th>
                <th>Qty</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.product_id}>
                  <td>{r.product_sku}</td>
                  <td>{r.product_name}</td>
                  <td>
                    {r.total_quantity} {r.uom_code}
                  </td>
                  <td>
                    <span className={`badge ${r.total_quantity <= 0 ? 'OUT_OF_STOCK' : r.is_low_stock ? 'LOW_STOCK' : 'NORMAL'}`}>
                      {r.total_quantity <= 0 ? 'OUT OF STOCK' : r.is_low_stock ? 'LOW STOCK' : 'NORMAL'}
                    </span>
                  </td>
                </tr>
              ))}
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
  const [error, setError] = useState('')

  const load = () => {
    stockApi
      .ledger({
        operation_type: operation || undefined,
        warehouse_id: warehouseId ? Number(warehouseId) : undefined,
      })
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }

  useEffect(() => {
    masterApi.warehouses().then(setWarehouses).catch((err) => setError(apiError(err)))
    load()
  }, [])

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Move history</h1>
          <p>Append-only stock ledger. Corrections must be new compensating documents.</p>
        </div>
      </div>
      <div className="toolbar">
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
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No ledger entries.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>When</th>
                <th>Product</th>
                <th>Location</th>
                <th>Op</th>
                <th>Ref</th>
                <th>Before</th>
                <th>Change</th>
                <th>After</th>
                <th>User</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((e) => (
                <tr key={e.id}>
                  <td>{new Date(e.created_at).toLocaleString()}</td>
                  <td>
                    {e.product_name}
                    <div className="muted">{e.product_sku}</div>
                  </td>
                  <td>
                    {e.warehouse_name} / {e.location_name}
                  </td>
                  <td>{e.operation_type}</td>
                  <td>{e.reference_id}</td>
                  <td>{e.quantity_before}</td>
                  <td>
                    {e.quantity_change > 0 ? '+' : ''}
                    {e.quantity_change}
                  </td>
                  <td>{e.quantity_after}</td>
                  <td>{e.created_by_name || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
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
  const raw = localStorage.getItem('ss_user')
  const user = raw ? (JSON.parse(raw) as { full_name: string; email: string; role: string }) : null
  return (
    <div className="panel" style={{ maxWidth: 520 }}>
      <h1>My profile</h1>
      {user ? (
        <div className="detail-meta">
          <div className="meta-box">
            <span>Name</span>
            {user.full_name}
          </div>
          <div className="meta-box">
            <span>Email</span>
            {user.email}
          </div>
          <div className="meta-box">
            <span>Role</span>
            {user.role.replaceAll('_', ' ')}
          </div>
        </div>
      ) : (
        <p className="empty">No profile loaded.</p>
      )}
    </div>
  )
}
