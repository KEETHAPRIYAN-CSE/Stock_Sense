import { useEffect, useState, type FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { apiError, masterApi, opsApi } from '../services/api'
import type { Adjustment, Delivery, Location, NamedId, Product, Receipt, Transfer, Warehouse } from '../types'

function Status({ value }: { value: string }) {
  return <span className={`badge ${value}`}>{value}</span>
}

function confirmAction(label: string) {
  return window.confirm(`${label}? This calls the inventory engine and cannot be undone from the UI.`)
}

type LineDraft = { product_id: string; quantity: string; uom_id: string }

function useMaster() {
  const [products, setProducts] = useState<Product[]>([])
  const [warehouses, setWarehouses] = useState<Warehouse[]>([])
  const [locations, setLocations] = useState<Location[]>([])
  const [suppliers, setSuppliers] = useState<NamedId[]>([])
  const [customers, setCustomers] = useState<NamedId[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      masterApi.products(),
      masterApi.warehouses(),
      masterApi.locations(),
      masterApi.suppliers(),
      masterApi.customers(),
    ])
      .then(([p, w, l, s, c]) => {
        setProducts(p)
        setWarehouses(w)
        setLocations(l)
        setSuppliers(s)
        setCustomers(c)
      })
      .catch((err) => setError(apiError(err)))
  }, [])

  return { products, warehouses, locations, suppliers, customers, error }
}

export function ReceiptsPage() {
  const [rows, setRows] = useState<Receipt[]>([])
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    opsApi
      .receipts()
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }, [])

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Receipts</h1>
          <p>Inbound stock. Validation increases balances and writes RECEIPT ledger rows.</p>
        </div>
        <Link className="btn" to="/receipts/new">
          Create receipt
        </Link>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No receipts yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Number</th>
                <th>Supplier</th>
                <th>Location</th>
                <th>Qty</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="clickable" onClick={() => navigate(`/receipts/${r.id}`)}>
                  <td>{r.receipt_number}</td>
                  <td>{r.supplier_name}</td>
                  <td>{r.destination_location_name}</td>
                  <td>{r.total_quantity}</td>
                  <td>
                    <Status value={r.status} />
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

export function ReceiptCreatePage() {
  const nav = useNavigate()
  const master = useMaster()
  const [supplierId, setSupplierId] = useState('')
  const [warehouseId, setWarehouseId] = useState('')
  const [locationId, setLocationId] = useState('')
  const [lines, setLines] = useState<LineDraft[]>([{ product_id: '', quantity: '100', uom_id: '' }])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (master.suppliers[0] && !supplierId) setSupplierId(String(master.suppliers[0].id))
    if (master.warehouses[0] && !warehouseId) setWarehouseId(String(master.warehouses[0].id))
  }, [master, supplierId, warehouseId])

  useEffect(() => {
    const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)
    if (locs[0]) setLocationId(String(locs[0].id))
  }, [warehouseId, master.locations])

  useEffect(() => {
    if (!master.products[0]) return
    setLines((prev) =>
      prev.map((line) => {
        const product = master.products.find((p) => String(p.id) === line.product_id) || master.products[0]
        return {
          product_id: String(product.id),
          quantity: line.quantity,
          uom_id: String(product.uom_id),
        }
      }),
    )
  }, [master.products])

  const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const created = await opsApi.createReceipt({
        supplier_id: Number(supplierId),
        warehouse_id: Number(warehouseId),
        destination_location_id: Number(locationId),
        items: lines.map((l) => ({
          product_id: Number(l.product_id),
          quantity: Number(l.quantity),
          uom_id: Number(l.uom_id),
        })),
      })
      nav(`/receipts/${created.id}`)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel">
      <h1>Create receipt</h1>
      {master.error || error ? <div className="alert">{master.error || error}</div> : null}
      <form className="form" onSubmit={onSubmit}>
        <label>
          Supplier
          <select value={supplierId} onChange={(e) => setSupplierId(e.target.value)}>
            {master.suppliers.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Warehouse
          <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)}>
            {master.warehouses.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Destination location
          <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            {locs.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name}
              </option>
            ))}
          </select>
        </label>
        <div>
          <strong>Lines</strong>
          {lines.map((line, idx) => (
            <div className="line-row" key={idx}>
              <select
                value={line.product_id}
                onChange={(e) => {
                  const p = master.products.find((x) => String(x.id) === e.target.value)
                  const next = [...lines]
                  next[idx] = { ...line, product_id: e.target.value, uom_id: p ? String(p.uom_id) : line.uom_id }
                  setLines(next)
                }}
              >
                {master.products.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.sku} — {p.name}
                  </option>
                ))}
              </select>
              <input
                type="number"
                min={0.0001}
                step="any"
                value={line.quantity}
                onChange={(e) => {
                  const next = [...lines]
                  next[idx] = { ...line, quantity: e.target.value }
                  setLines(next)
                }}
              />
              <span className="muted">UOM {line.uom_id}</span>
              <button
                type="button"
                className="btn secondary"
                onClick={() => setLines(lines.filter((_, i) => i !== idx))}
                disabled={lines.length === 1}
              >
                Remove
              </button>
            </div>
          ))}
          <button
            type="button"
            className="btn secondary"
            onClick={() =>
              setLines([
                ...lines,
                {
                  product_id: String(master.products[0]?.id || ''),
                  quantity: '1',
                  uom_id: String(master.products[0]?.uom_id || ''),
                },
              ])
            }
          >
            Add line
          </button>
        </div>
        <button className="btn" disabled={busy}>
          Save draft
        </button>
      </form>
    </div>
  )
}

export function ReceiptDetailPage() {
  const { id } = useParams()
  const [doc, setDoc] = useState<Receipt | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const load = () => {
    if (!id) return
    opsApi
      .receipt(Number(id))
      .then(setDoc)
      .catch((err) => setError(apiError(err)))
  }

  useEffect(load, [id])

  const run = async (fn: () => Promise<Receipt>, label: string) => {
    if (!confirmAction(label)) return
    setBusy(true)
    setError('')
    try {
      setDoc(await fn())
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  if (!doc) return error ? <div className="alert">{error}</div> : <p className="muted">Loading…</p>
  const open = !['DONE', 'CANCELED'].includes(doc.status)

  return (
    <>
      <div className="page-head">
        <div>
          <h1>{doc.receipt_number}</h1>
          <p>
            {doc.supplier_name} → {doc.destination_location_name}
          </p>
        </div>
        <div className="row-actions">
          {open ? (
            <>
              <button className="btn" disabled={busy} onClick={() => run(() => opsApi.validateReceipt(doc.id), 'Validate receipt and increase stock')}>
                Validate
              </button>
              <button className="btn danger" disabled={busy} onClick={() => run(() => opsApi.cancelReceipt(doc.id), 'Cancel receipt')}>
                Cancel
              </button>
            </>
          ) : null}
          <Link className="btn secondary" to="/receipts">
            Back
          </Link>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="detail-meta">
        <div className="meta-box">
          <span>Status</span>
          <Status value={doc.status} />
        </div>
        <div className="meta-box">
          <span>Warehouse</span>
          {doc.warehouse_name}
        </div>
        <div className="meta-box">
          <span>Created by</span>
          {doc.created_by_name || '—'}
        </div>
      </div>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Qty</th>
              <th>UOM</th>
            </tr>
          </thead>
          <tbody>
            {doc.items?.map((it) => (
              <tr key={it.id}>
                <td>
                  {it.product_name}
                  <div className="muted">{it.product_sku}</div>
                </td>
                <td>{it.quantity}</td>
                <td>{it.uom_code}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

export function DeliveriesPage() {
  const [rows, setRows] = useState<Delivery[]>([])
  const [error, setError] = useState('')
  const navigate = useNavigate()
  useEffect(() => {
    opsApi
      .deliveries()
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }, [])
  return (
    <>
      <div className="page-head">
        <div>
          <h1>Delivery orders</h1>
          <p>Pick → pack → validate. Validation refuses quantities above available stock.</p>
        </div>
        <Link className="btn" to="/deliveries/new">
          Create delivery
        </Link>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No deliveries yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Number</th>
                <th>Customer</th>
                <th>Source</th>
                <th>Qty</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="clickable" onClick={() => navigate(`/deliveries/${r.id}`)}>
                  <td>{r.delivery_number}</td>
                  <td>{r.customer_name}</td>
                  <td>{r.source_location_name}</td>
                  <td>{r.total_quantity}</td>
                  <td>
                    <Status value={r.status} />
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

export function DeliveryCreatePage() {
  const nav = useNavigate()
  const master = useMaster()
  const [customerId, setCustomerId] = useState('')
  const [warehouseId, setWarehouseId] = useState('')
  const [locationId, setLocationId] = useState('')
  const [lines, setLines] = useState<LineDraft[]>([{ product_id: '', quantity: '20', uom_id: '' }])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (master.customers[0] && !customerId) setCustomerId(String(master.customers[0].id))
    if (master.warehouses[0] && !warehouseId) setWarehouseId(String(master.warehouses[0].id))
  }, [master, customerId, warehouseId])
  useEffect(() => {
    const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)
    if (locs[0]) setLocationId(String(locs[0].id))
  }, [warehouseId, master.locations])
  useEffect(() => {
    if (!master.products[0]) return
    setLines((prev) =>
      prev.map((line) => {
        const product = master.products.find((p) => String(p.id) === line.product_id) || master.products[0]
        return { product_id: String(product.id), quantity: line.quantity, uom_id: String(product.uom_id) }
      }),
    )
  }, [master.products])

  const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const created = await opsApi.createDelivery({
        customer_id: Number(customerId),
        warehouse_id: Number(warehouseId),
        source_location_id: Number(locationId),
        items: lines.map((l) => ({ product_id: Number(l.product_id), quantity: Number(l.quantity), uom_id: Number(l.uom_id) })),
      })
      nav(`/deliveries/${created.id}`)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel">
      <h1>Create delivery</h1>
      {master.error || error ? <div className="alert">{master.error || error}</div> : null}
      <form className="form" onSubmit={onSubmit}>
        <label>
          Customer
          <select value={customerId} onChange={(e) => setCustomerId(e.target.value)}>
            {master.customers.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Warehouse
          <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)}>
            {master.warehouses.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Source location
          <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            {locs.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name}
              </option>
            ))}
          </select>
        </label>
        {lines.map((line, idx) => (
          <div className="line-row" key={idx}>
            <select
              value={line.product_id}
              onChange={(e) => {
                const p = master.products.find((x) => String(x.id) === e.target.value)
                const next = [...lines]
                next[idx] = { ...line, product_id: e.target.value, uom_id: p ? String(p.uom_id) : line.uom_id }
                setLines(next)
              }}
            >
              {master.products.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.sku} — {p.name}
                </option>
              ))}
            </select>
            <input
              type="number"
              min={0.0001}
              step="any"
              value={line.quantity}
              onChange={(e) => {
                const next = [...lines]
                next[idx] = { ...line, quantity: e.target.value }
                setLines(next)
              }}
            />
          </div>
        ))}
        <button className="btn" disabled={busy}>
          Save draft
        </button>
      </form>
    </div>
  )
}

export function DeliveryDetailPage() {
  const { id } = useParams()
  const [doc, setDoc] = useState<Delivery | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const load = () => {
    if (!id) return
    opsApi
      .delivery(Number(id))
      .then(setDoc)
      .catch((err) => setError(apiError(err)))
  }
  useEffect(load, [id])
  const run = async (fn: () => Promise<Delivery>, label: string) => {
    if (!confirmAction(label)) return
    setBusy(true)
    setError('')
    try {
      setDoc(await fn())
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }
  if (!doc) return error ? <div className="alert">{error}</div> : <p className="muted">Loading…</p>
  const open = !['DONE', 'CANCELED'].includes(doc.status)
  return (
    <>
      <div className="page-head">
        <div>
          <h1>{doc.delivery_number}</h1>
          <p>
            {doc.customer_name} from {doc.source_location_name}
          </p>
        </div>
        <div className="row-actions">
          {open ? (
            <>
              <button className="btn secondary" disabled={busy} onClick={() => run(() => opsApi.pickDelivery(doc.id), 'Mark picked')}>
                Pick
              </button>
              <button className="btn secondary" disabled={busy} onClick={() => run(() => opsApi.packDelivery(doc.id), 'Mark packed')}>
                Pack
              </button>
              <button className="btn" disabled={busy} onClick={() => run(() => opsApi.validateDelivery(doc.id), 'Validate delivery and decrease stock')}>
                Validate
              </button>
              <button className="btn danger" disabled={busy} onClick={() => run(() => opsApi.cancelDelivery(doc.id), 'Cancel delivery')}>
                Cancel
              </button>
            </>
          ) : null}
          <Link className="btn secondary" to="/deliveries">
            Back
          </Link>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="detail-meta">
        <div className="meta-box">
          <span>Status</span>
          <Status value={doc.status} />
        </div>
      </div>
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Qty</th>
              <th>Picked</th>
              <th>Packed</th>
            </tr>
          </thead>
          <tbody>
            {doc.items?.map((it) => (
              <tr key={it.id}>
                <td>{it.product_name}</td>
                <td>{it.quantity}</td>
                <td>{it.picked_quantity}</td>
                <td>{it.packed_quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

export function TransfersPage() {
  const [rows, setRows] = useState<Transfer[]>([])
  const [error, setError] = useState('')
  const navigate = useNavigate()
  useEffect(() => {
    opsApi
      .transfers()
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }, [])
  return (
    <>
      <div className="page-head">
        <div>
          <h1>Internal transfers</h1>
          <p>Location changes only. Total quantity across the warehouse must stay the same.</p>
        </div>
        <Link className="btn" to="/transfers/new">
          Create transfer
        </Link>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No transfers yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Number</th>
                <th>From</th>
                <th>To</th>
                <th>Qty</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="clickable" onClick={() => navigate(`/transfers/${r.id}`)}>
                  <td>{r.transfer_number}</td>
                  <td>{r.source_location_name}</td>
                  <td>{r.destination_location_name}</td>
                  <td>{r.total_quantity}</td>
                  <td>
                    <Status value={r.status} />
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

export function TransferCreatePage() {
  const nav = useNavigate()
  const master = useMaster()
  const [warehouseId, setWarehouseId] = useState('')
  const [sourceId, setSourceId] = useState('')
  const [destId, setDestId] = useState('')
  const [lines, setLines] = useState<LineDraft[]>([{ product_id: '', quantity: '20', uom_id: '' }])
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (master.warehouses[0] && !warehouseId) setWarehouseId(String(master.warehouses[0].id))
  }, [master.warehouses, warehouseId])
  const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)
  useEffect(() => {
    if (locs[0]) setSourceId(String(locs[0].id))
    if (locs[1]) setDestId(String(locs[1].id))
    else if (locs[0]) setDestId(String(locs[0].id))
  }, [warehouseId, master.locations])
  useEffect(() => {
    if (!master.products[0]) return
    setLines((prev) =>
      prev.map((line) => {
        const product = master.products.find((p) => String(p.id) === line.product_id) || master.products[0]
        return { product_id: String(product.id), quantity: line.quantity, uom_id: String(product.uom_id) }
      }),
    )
  }, [master.products])

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const created = await opsApi.createTransfer({
        warehouse_id: Number(warehouseId),
        source_location_id: Number(sourceId),
        destination_location_id: Number(destId),
        items: lines.map((l) => ({ product_id: Number(l.product_id), quantity: Number(l.quantity), uom_id: Number(l.uom_id) })),
      })
      nav(`/transfers/${created.id}`)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel">
      <h1>Create transfer</h1>
      {master.error || error ? <div className="alert">{master.error || error}</div> : null}
      <form className="form" onSubmit={onSubmit}>
        <label>
          Warehouse
          <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)}>
            {master.warehouses.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Source
          <select value={sourceId} onChange={(e) => setSourceId(e.target.value)}>
            {locs.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Destination
          <select value={destId} onChange={(e) => setDestId(e.target.value)}>
            {locs.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name}
              </option>
            ))}
          </select>
        </label>
        {lines.map((line, idx) => (
          <div className="line-row" key={idx}>
            <select
              value={line.product_id}
              onChange={(e) => {
                const p = master.products.find((x) => String(x.id) === e.target.value)
                const next = [...lines]
                next[idx] = { ...line, product_id: e.target.value, uom_id: p ? String(p.uom_id) : line.uom_id }
                setLines(next)
              }}
            >
              {master.products.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.sku} — {p.name}
                </option>
              ))}
            </select>
            <input
              type="number"
              min={0.0001}
              step="any"
              value={line.quantity}
              onChange={(e) => {
                const next = [...lines]
                next[idx] = { ...line, quantity: e.target.value }
                setLines(next)
              }}
            />
          </div>
        ))}
        <button className="btn" disabled={busy}>
          Save
        </button>
      </form>
    </div>
  )
}

export function TransferDetailPage() {
  const { id } = useParams()
  const [doc, setDoc] = useState<Transfer | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  useEffect(() => {
    if (!id) return
    opsApi
      .transfer(Number(id))
      .then(setDoc)
      .catch((err) => setError(apiError(err)))
  }, [id])
  if (!doc) return error ? <div className="alert">{error}</div> : <p className="muted">Loading…</p>
  const open = !['DONE', 'CANCELED'].includes(doc.status)
  return (
    <>
      <div className="page-head">
        <div>
          <h1>{doc.transfer_number}</h1>
          <p>
            {doc.source_location_name} → {doc.destination_location_name}
          </p>
        </div>
        <div className="row-actions">
          {open ? (
            <>
              <button
                className="btn"
                disabled={busy}
                onClick={async () => {
                  if (!confirmAction('Validate transfer')) return
                  setBusy(true)
                  try {
                    setDoc(await opsApi.validateTransfer(doc.id))
                  } catch (err) {
                    setError(apiError(err))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Validate
              </button>
              <button
                className="btn danger"
                disabled={busy}
                onClick={async () => {
                  if (!confirmAction('Cancel transfer')) return
                  setBusy(true)
                  try {
                    setDoc(await opsApi.cancelTransfer(doc.id))
                  } catch (err) {
                    setError(apiError(err))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Cancel
              </button>
            </>
          ) : null}
          <Link className="btn secondary" to="/transfers">
            Back
          </Link>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Qty</th>
            </tr>
          </thead>
          <tbody>
            {doc.items?.map((it) => (
              <tr key={it.id}>
                <td>{it.product_name}</td>
                <td>{it.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}

export function AdjustmentsPage() {
  const [rows, setRows] = useState<Adjustment[]>([])
  const [error, setError] = useState('')
  const navigate = useNavigate()
  useEffect(() => {
    opsApi
      .adjustments()
      .then(setRows)
      .catch((err) => setError(apiError(err)))
  }, [])
  return (
    <>
      <div className="page-head">
        <div>
          <h1>Inventory adjustments</h1>
          <p>Physical count vs system quantity. Difference writes an ADJUSTMENT ledger entry.</p>
        </div>
        <Link className="btn" to="/adjustments/new">
          New count
        </Link>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        {rows.length === 0 ? (
          <p className="empty">No adjustments yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Number</th>
                <th>Location</th>
                <th>Reason</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id} className="clickable" onClick={() => navigate(`/adjustments/${r.id}`)}>
                  <td>{r.adjustment_number}</td>
                  <td>{r.location_name}</td>
                  <td>{r.reason || '—'}</td>
                  <td>
                    <Status value={r.status} />
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

export function AdjustmentCreatePage() {
  const nav = useNavigate()
  const master = useMaster()
  const [warehouseId, setWarehouseId] = useState('')
  const [locationId, setLocationId] = useState('')
  const [reason, setReason] = useState('Damaged goods')
  const [productId, setProductId] = useState('')
  const [counted, setCounted] = useState('0')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (master.warehouses[0] && !warehouseId) setWarehouseId(String(master.warehouses[0].id))
    if (master.products[0] && !productId) setProductId(String(master.products[0].id))
  }, [master, warehouseId, productId])
  const locs = master.locations.filter((l) => !warehouseId || String(l.warehouse_id) === warehouseId)
  useEffect(() => {
    if (locs[0]) setLocationId(String(locs[0].id))
  }, [warehouseId, master.locations])

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const created = await opsApi.createAdjustment({
        warehouse_id: Number(warehouseId),
        location_id: Number(locationId),
        reason,
        items: [{ product_id: Number(productId), counted_quantity: Number(counted) }],
      })
      nav(`/adjustments/${created.id}`)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel">
      <h1>Record physical count</h1>
      {master.error || error ? <div className="alert">{master.error || error}</div> : null}
      <form className="form" onSubmit={onSubmit}>
        <label>
          Warehouse
          <select value={warehouseId} onChange={(e) => setWarehouseId(e.target.value)}>
            {master.warehouses.map((w) => (
              <option key={w.id} value={w.id}>
                {w.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Location
          <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            {locs.map((l) => (
              <option key={l.id} value={l.id}>
                {l.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Product
          <select value={productId} onChange={(e) => setProductId(e.target.value)}>
            {master.products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.sku} — {p.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Counted quantity
          <input type="number" min={0} step="any" value={counted} onChange={(e) => setCounted(e.target.value)} />
        </label>
        <label>
          Reason
          <input value={reason} onChange={(e) => setReason(e.target.value)} />
        </label>
        <button className="btn" disabled={busy}>
          Save draft
        </button>
      </form>
    </div>
  )
}

export function AdjustmentDetailPage() {
  const { id } = useParams()
  const [doc, setDoc] = useState<Adjustment | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  useEffect(() => {
    if (!id) return
    opsApi
      .adjustment(Number(id))
      .then(setDoc)
      .catch((err) => setError(apiError(err)))
  }, [id])
  if (!doc) return error ? <div className="alert">{error}</div> : <p className="muted">Loading…</p>
  const open = !['DONE', 'CANCELED'].includes(doc.status)
  return (
    <>
      <div className="page-head">
        <div>
          <h1>{doc.adjustment_number}</h1>
          <p>
            {doc.location_name} · {doc.reason}
          </p>
        </div>
        <div className="row-actions">
          {open ? (
            <>
              <button
                className="btn"
                disabled={busy}
                onClick={async () => {
                  if (!confirmAction('Validate adjustment')) return
                  setBusy(true)
                  try {
                    setDoc(await opsApi.validateAdjustment(doc.id))
                  } catch (err) {
                    setError(apiError(err))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Validate
              </button>
              <button
                className="btn danger"
                disabled={busy}
                onClick={async () => {
                  if (!confirmAction('Cancel adjustment')) return
                  setBusy(true)
                  try {
                    setDoc(await opsApi.cancelAdjustment(doc.id))
                  } catch (err) {
                    setError(apiError(err))
                  } finally {
                    setBusy(false)
                  }
                }}
              >
                Cancel
              </button>
            </>
          ) : null}
          <Link className="btn secondary" to="/adjustments">
            Back
          </Link>
        </div>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      <div className="panel">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>System</th>
              <th>Counted</th>
              <th>Diff</th>
            </tr>
          </thead>
          <tbody>
            {doc.items?.map((it) => (
              <tr key={it.id}>
                <td>{it.product_name}</td>
                <td>{it.system_quantity}</td>
                <td>{it.counted_quantity}</td>
                <td>{it.difference}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
