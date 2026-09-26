import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff } from 'lucide-react'
import { apiError, authApi } from '../services/api'
import { useAuth } from '../context/AuthContext'

function AuthBrand() {
  return (
    <div className="auth-brand">
      <div className="brand-mark" aria-hidden="true">S</div>
      <div>
        <strong>StockSense</strong>
        <span>Inventory intelligence</span>
      </div>
    </div>
  )
}

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('manager@stocksense.com')
  const [password, setPassword] = useState('admin123')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      await login(email, password)
      navigate('/')
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <AuthBrand />
        <h1>Sign in</h1>
        <p>Secure access to your live inventory workspace.</p>
        {error ? <div className="alert">{error}</div> : null}
        <form className="form" onSubmit={onSubmit}>
          <label>
            Login ID or email
            <input type="email" autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            Password
            <span className="password-field">
              <input type={showPassword ? 'text' : 'password'} autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              <button
                className="password-toggle"
                type="button"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                onClick={() => setShowPassword((visible) => !visible)}
              >
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </span>
          </label>
          <button className="btn" disabled={busy}>
            {busy ? 'Signing in…' : 'Login'}
          </button>
        </form>
        <p>
          <Link to="/register">Create account</Link> · <Link to="/forgot-password">Forgot password</Link>
        </p>
      </div>
    </div>
  )
}

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('INVENTORY_MANAGER')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      await register({ full_name: fullName, email, password, role })
      navigate('/')
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <AuthBrand />
        <h1>Create account</h1>
        <p>Inventory managers and warehouse staff share the same operational workspace.</p>
        {error ? <div className="alert">{error}</div> : null}
        <form className="form" onSubmit={onSubmit}>
          <label>
            Full name
            <input value={fullName} onChange={(e) => setFullName(e.target.value)} required />
          </label>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            Password
            <input type="password" minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} required />
          </label>
          <label>
            Role
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="INVENTORY_MANAGER">Inventory Manager</option>
              <option value="WAREHOUSE_STAFF">Warehouse Staff</option>
            </select>
          </label>
          <button className="btn" disabled={busy}>
            {busy ? 'Creating…' : 'Sign up'}
          </button>
        </form>
        <p>
          <Link to="/login">Back to login</Link>
        </p>
      </div>
    </div>
  )
}

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('manager@stocksense.com')
  const [message, setMessage] = useState('')
  const [otp, setOtp] = useState('')
  const [error, setError] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const res = await authApi.forgot(email)
      setMessage(res.message)
      setOtp(res.dev_otp || '')
    } catch (err) {
      setError(apiError(err))
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <h1>Forgot password</h1>
        <p>A one-time code is issued for reset. In development the OTP is shown here for the demo.</p>
        {error ? <div className="alert">{error}</div> : null}
        {message ? <div className="alert ok">{message}{otp ? ` Demo OTP: ${otp}` : ''}</div> : null}
        <form className="form" onSubmit={onSubmit}>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <button className="btn">Send OTP</button>
        </form>
        <p>
          <Link to="/reset-password">I have an OTP</Link> · <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  )
}

export function ResetPasswordPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('manager@stocksense.com')
  const [otp, setOtp] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [ok, setOk] = useState('')

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await authApi.reset(email, otp, password)
      setOk('Password updated. You can sign in.')
      setTimeout(() => navigate('/login'), 800)
    } catch (err) {
      setError(apiError(err))
    }
  }

  return (
    <div className="auth-wrap">
      <div className="card auth-card">
        <h1>Reset password</h1>
        {error ? <div className="alert">{error}</div> : null}
        {ok ? <div className="alert ok">{ok}</div> : null}
        <form className="form" onSubmit={onSubmit}>
          <label>
            Email
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            OTP
            <input value={otp} onChange={(e) => setOtp(e.target.value)} minLength={6} maxLength={6} required />
          </label>
          <label>
            New password
            <input type="password" minLength={6} value={password} onChange={(e) => setPassword(e.target.value)} required />
          </label>
          <button className="btn">Reset</button>
        </form>
      </div>
    </div>
  )
}
