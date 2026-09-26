import { useEffect, useState, type FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { apiError, masterApi } from '../services/api'
import type { NamedId, Product } from '../types'

export function ProductsPage() {
  const [rows, setRows] = useState<Product[]>([])
  const [search, setSearch] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const load = () => {
    setLoading(true)
    masterApi
      .products({ search: search || undefined })
      .then(setRows)
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [])

  return (
    <>
      <div className="page-head">
        <div>
          <h1>Products</h1>
          <p>Search by SKU or name. Stock totals come from location balances.</p>
        </div>
        <Link className="btn" to="/products/new">
          New product
        </Link>
      </div>
      <div className="toolbar">
        <input placeholder="SKU or name" value={search} onChange={(e) => setSearch(e.target.value)} />
        <button className="btn secondary" onClick={load}>
          Search
        </button>
      </div>
      {error ? <div className="alert">{error}</div> : null}
      {loading ? (
        <p className="muted">Loading products…</p>
      ) : rows.length === 0 ? (
        <p className="empty">No products found.</p>
      ) : (
        <div className="panel">
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Name</th>
                <th>Category</th>
                <th>Stock</th>
                <th>Reorder</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((p) => (
                <tr key={p.id} className="clickable" onClick={() => navigate(`/products/${p.id}`)}>
                  <td>{p.sku}</td>
                  <td>{p.name}</td>
                  <td>{p.category_name || '—'}</td>
                  <td>
                    {p.total_stock} {p.uom_code}
                  </td>
                  <td>{p.reorder_level}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  )
}

export function ProductFormPage() {
  const navigate = useNavigate()
  const [categories, setCategories] = useState<NamedId[]>([])
  const [uoms, setUoms] = useState<NamedId[]>([])
  const [locations, setLocations] = useState<NamedId[]>([])
  const [name, setName] = useState('')
  const [sku, setSku] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [uomId, setUomId] = useState('')
  const [reorder, setReorder] = useState('0')
  const [initial, setInitial] = useState('0')
  const [locationId, setLocationId] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    Promise.all([masterApi.categories(), masterApi.uoms(), masterApi.locations()])
      .then(([c, u, l]) => {
        setCategories(c)
        setUoms(u)
        setLocations(l)
        if (u[0]) setUomId(String(u[0].id))
        if (c[0]) setCategoryId(String(c[0].id))
        if (l[0]) setLocationId(String(l[0].id))
      })
      .catch((err) => setError(apiError(err)))
  }, [])

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const created = await masterApi.createProduct({
        name,
        sku,
        category_id: categoryId ? Number(categoryId) : null,
        uom_id: Number(uomId),
        reorder_level: Number(reorder),
        initial_stock: Number(initial),
        initial_location_id: locationId ? Number(locationId) : null,
      })
      navigate(`/products/${created.id}`)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="panel" style={{ maxWidth: 640 }}>
      <h1>New product</h1>
      {error ? <div className="alert">{error}</div> : null}
      <form className="form" onSubmit={onSubmit}>
        <label>
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          SKU
          <input value={sku} onChange={(e) => setSku(e.target.value)} required />
        </label>
        <label>
          Category
          <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Unit
          <select value={uomId} onChange={(e) => setUomId(e.target.value)} required>
            {uoms.map((u) => (
              <option key={u.id} value={u.id}>
                {u.code || u.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Reorder level
          <input type="number" min={0} step="any" value={reorder} onChange={(e) => setReorder(e.target.value)} />
        </label>
        <label>
          Opening stock (writes INITIAL ledger if location set)
          <input type="number" min={0} step="any" value={initial} onChange={(e) => setInitial(e.target.value)} />
        </label>
        <label>
          Opening location
          <select value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            {locations.map((l) => (
              <option key={l.id} value={l.id}>
                {l.warehouse_name ? `${l.warehouse_name} / ${l.name}` : l.name}
              </option>
            ))}
          </select>
        </label>
        <div className="row-actions">
          <button className="btn" disabled={busy}>
            Save
          </button>
          <button className="btn secondary" type="button" onClick={() => navigate('/products')}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

export function ProductDetailPage() {
  const { id } = useParams()
  const [product, setProduct] = useState<Product | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return
    masterApi
      .product(Number(id))
      .then(setProduct)
      .catch((err) => setError(apiError(err)))
  }, [id])

  if (error) return <div className="alert">{error}</div>
  if (!product) return <p className="muted">Loading product…</p>

  return (
    <>
      <div className="page-head">
        <div>
          <h1>{product.name}</h1>
          <p>
            {product.sku} · {product.category_name} · {product.uom_code}
          </p>
        </div>
        <Link className="btn secondary" to="/products">
          Back
        </Link>
      </div>
      <div className="kpis">
        <div className="kpi">
          <span>Total stock</span>
          <strong>{product.total_stock}</strong>
        </div>
        <div className="kpi">
          <span>Reorder level</span>
          <strong>{product.reorder_level}</strong>
        </div>
      </div>
      <div className="panel">
        <h3>Stock by location</h3>
        {!product.location_stocks?.length ? (
          <p className="empty">No location balances yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Warehouse</th>
                <th>Location</th>
                <th>Qty</th>
              </tr>
            </thead>
            <tbody>
              {product.location_stocks.map((s) => (
                <tr key={s.location_id}>
                  <td>{s.warehouse_name}</td>
                  <td>{s.location_name}</td>
                  <td>{s.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  )
}
