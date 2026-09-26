import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import {
  ArrowLeftRight,
  Boxes,
  ClipboardList,
  History,
  LayoutDashboard,
  LogOut,
  Package,
  Truck,
  UserRound,
  Warehouse,
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/stock', label: 'Stock', icon: Boxes },
  { to: '/products', label: 'Products', icon: Package },
  { to: '/receipts', label: 'Receipts', icon: ClipboardList },
  { to: '/deliveries', label: 'Delivery Orders', icon: Truck },
  { to: '/transfers', label: 'Transfers', icon: ArrowLeftRight },
  { to: '/adjustments', label: 'Adjustments', icon: ClipboardList },
  { to: '/ledger', label: 'Move History', icon: History },
  { to: '/warehouses', label: 'Warehouse', icon: Warehouse },
  { to: '/profile', label: 'My Profile', icon: UserRound },
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">S</div>
          <div>
            <strong>StockSense</strong>
            <small>Inventory ledger</small>
          </div>
        </div>
        <div className="nav-group">Operations</div>
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} end={link.to === '/'} className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
            <link.icon size={16} />
            {link.label}
          </NavLink>
        ))}
        <div className="sidebar-foot">
          <div>{user?.full_name}</div>
          <div>{user?.role.replaceAll('_', ' ')}</div>
          <button
            className="btn secondary"
            style={{ marginTop: 10, width: '100%' }}
            onClick={() => {
              logout()
              navigate('/login')
            }}
          >
            <LogOut size={14} /> Logout
          </button>
        </div>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
