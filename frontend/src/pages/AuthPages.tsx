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
        <span>Inventory Intelligence</span>
      </div>
    </div>
  )
}

function GoogleButton({ onClick, label = 'Sign in with Google' }: { onClick: () => void; label?: string }) {
  return (
    <button
      type="button"
      className="btn secondary"
      style={{
        width: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 10,
        padding: '11px 16px',
        fontWeight: 600,
        backgroundColor: '#ffffff',
        borderColor: '#d5cec0',
        color: '#2e2a27',
      }}
      onClick={onClick}
    >
      <svg width="18" height="18" viewBox="0 0 24 24">
        <path
          fill="#EA4335"
          d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.9C6.2 7.3 8.9 5 12 5z"
        />
        <path
          fill="#4285F4"
          d="M23.5 12.3c0-.8-.1-1.7-.2-2.3H12v4.6h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.9z"
        />
        <path
          fill="#FBBC05"
          d="M5.3 14.7c-.2-.7-.4-1.5-.4-2.7s.1-2 .4-2.7L1.6 6.4C.6 8.3 0 10.1 0 12s.6 3.7 1.6 5.6l3.7-2.9z"
        />
        <path
          fill="#34A853"
          d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.3-6.7-5.3L1.6 16c1.9 3.8 5.8 7 10.4 7z"
        />
      </svg>
      {label}
    </button>
  )
}

function AuthFooter() {
  return (
    <div className="auth-footer-links">
      <span>© StockSense</span>
      <span>·</span>
      <a href="#terms" onClick={(e) => e.preventDefault()}>Terms of Use</a>
      <span>·</span>
      <a href="#privacy" onClick={(e) => e.preventDefault()}>Privacy Policy</a>
    </div>
  )
}

export function LoginPage() {
  const { login, loginWithGoogle } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('manager@stocksense.com')
  const [password, setPassword] = useState('admin123')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onGoogleLogin = async () => {
    const googleEmail = window.prompt(
      'Enter your Google / Gmail account:',
      'keethapriyan.71382402066@sritcbe.ac.in',
    )
    if (!googleEmail || !googleEmail.trim()) return

    setBusy(true)
    setError('')
    try {
      await loginWithGoogle({
        email: googleEmail.trim(),
        full_name: googleEmail.split('@')[0],
      })
      navigate('/')
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

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
      {/* Primary Sign In Card */}
      <div className="auth-card">
        <AuthBrand />
        <h1>Sign in to StockSense</h1>
        <p className="subtitle">Enterprise Inventory Management & Intelligence</p>
        
        {error ? <div className="alert">{error}</div> : null}

        <form className="form" onSubmit={onSubmit}>
          <label>
            Username or email
            <input
              type="email"
              autoComplete="username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. manager@stocksense.com"
              required
            />
          </label>
          <label>
            Password
            <span className="password-field">
              <input
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
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
          <button className="btn" style={{ width: '100%', padding: '12px', marginTop: '4px' }} disabled={busy}>
            {busy ? 'Signing in…' : 'Sign in'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 18 }}>
          <Link to="/forgot-password" className="auth-link">
            Forgot password?
          </Link>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '22px 0 16px' }}>
          <div style={{ flex: 1, height: 1, background: '#ded7c6' }} />
          <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
            or continue with
          </span>
          <div style={{ flex: 1, height: 1, background: '#ded7c6' }} />
        </div>

        <GoogleButton onClick={onGoogleLogin} label="Sign in with Google" />
      </div>

      {/* Secondary Card: Don't have an account? */}
      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Don't have a StockSense Account?</h2>
        <Link to="/register" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Create Account
        </Link>
      </div>

      <AuthFooter />
    </div>
  )
}

export function RegisterPage() {
  const { register, loginWithGoogle } = useAuth()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('INVENTORY_MANAGER')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onGoogleSignUp = async () => {
    const googleEmail = window.prompt(
      'Enter your Google / Gmail account:',
      'keethapriyan.71382402066@sritcbe.ac.in',
    )
    if (!googleEmail || !googleEmail.trim()) return

    setBusy(true)
    setError('')
    try {
      await loginWithGoogle({
        email: googleEmail.trim(),
        full_name: googleEmail.split('@')[0],
        role: role,
      })
      navigate('/')
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

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
      <div className="auth-card">
        <AuthBrand />
        <h1>Create your Account</h1>
        <p className="subtitle">Join your enterprise inventory operations team</p>
        
        {error ? <div className="alert">{error}</div> : null}

        <form className="form" onSubmit={onSubmit}>
          <label>
            Full name
            <input
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="e.g. Alex Morgan"
              required
            />
          </label>
          <label>
            Corporate email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="alex@company.com"
              required
            />
          </label>
          <label>
            Password (6+ characters)
            <input
              type="password"
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Choose a strong password"
              required
            />
          </label>
          <label>
            Assigned role
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              <option value="INVENTORY_MANAGER">Inventory Manager (Full Admin)</option>
              <option value="WAREHOUSE_STAFF">Warehouse Staff (Pick & Receive)</option>
            </select>
          </label>
          <button className="btn" style={{ width: '100%', padding: '12px', marginTop: '4px' }} disabled={busy}>
            {busy ? 'Creating Account…' : 'Create Account'}
          </button>
        </form>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '22px 0 16px' }}>
          <div style={{ flex: 1, height: 1, background: '#ded7c6' }} />
          <span style={{ fontSize: 11, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
            or register with
          </span>
          <div style={{ flex: 1, height: 1, background: '#ded7c6' }} />
        </div>

        <GoogleButton onClick={onGoogleSignUp} label="Sign up with Google" />
      </div>

      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Already have a StockSense Account?</h2>
        <Link to="/login" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Sign In
        </Link>
      </div>

      <AuthFooter />
    </div>
  )
}

export function ForgotPasswordPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError('')
    setMessage('')
    try {
      const res = await authApi.forgot(email)
      setMessage(res.message || 'If your email is registered, you will receive an OTP in your inbox shortly.')
      setTimeout(() => {
        navigate(`/reset-password?email=${encodeURIComponent(email)}`)
      }, 1500)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <AuthBrand />
        <h1>Reset Password</h1>
        <p className="subtitle">Enter your registered email to receive a secure 6-digit OTP</p>
        
        {error ? <div className="alert">{error}</div> : null}
        {message ? (
          <div className="alert ok" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 6 }}>
            <div>{message}</div>
            <span style={{ fontSize: 12, opacity: 0.85 }}>Redirecting to verification page…</span>
          </div>
        ) : null}

        <form className="form" onSubmit={onSubmit}>
          <label>
            Registered Email Address
            <input
              type="email"
              placeholder="e.g. yourname@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <button className="btn" style={{ width: '100%', padding: '12px', marginTop: '4px' }} disabled={busy}>
            {busy ? 'Sending OTP to Email…' : 'Send Verification Code'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 18 }}>
          <Link to="/reset-password" className="auth-link">
            I already have an OTP code
          </Link>
        </div>
      </div>

      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Remember your credentials?</h2>
        <Link to="/login" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Back to Sign In
        </Link>
      </div>

      <AuthFooter />
    </div>
  )
}

export function ResetPasswordPage() {
  const navigate = useNavigate()
  const searchParams = new URLSearchParams(window.location.search)
  const initialEmail = searchParams.get('email') || ''

  const [email, setEmail] = useState(initialEmail)
  const [otp, setOtp] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [ok, setOk] = useState('')
  const [busy, setBusy] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }
    if (password.length < 6) {
      setError('Password must be at least 6 characters.')
      return
    }
    setBusy(true)
    try {
      await authApi.reset(email, otp.trim(), password)
      setOk('Password updated successfully. Redirecting to login…')
      setTimeout(() => navigate('/login'), 1200)
    } catch (err) {
      setError(apiError(err))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <AuthBrand />
        <h1>Set New Password</h1>
        <p className="subtitle">Enter the 6-digit code received via email and your new password</p>
        
        {error ? <div className="alert">{error}</div> : null}
        {ok ? <div className="alert ok">{ok}</div> : null}

        <form className="form" onSubmit={onSubmit}>
          <label>
            Email Address
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </label>
          <label>
            6-Digit Verification Code (OTP)
            <input
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              placeholder="e.g. 874158"
              minLength={6}
              maxLength={6}
              style={{ letterSpacing: 4, fontWeight: 700, fontSize: 16 }}
              required
            />
          </label>
          <label>
            New Password
            <span className="password-field">
              <input
                type={showPassword ? 'text' : 'password'}
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 6 characters"
                required
              />
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
          <label>
            Confirm New Password
            <input
              type={showPassword ? 'text' : 'password'}
              minLength={6}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Re-enter new password"
              required
            />
          </label>
          <button className="btn" style={{ width: '100%', padding: '12px', marginTop: '4px' }} disabled={busy}>
            {busy ? 'Verifying & Updating…' : 'Reset Password'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: 18 }}>
          <Link to="/forgot-password" className="auth-link">
            Request new OTP code
          </Link>
        </div>
      </div>

      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Done resetting?</h2>
        <Link to="/login" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Back to Sign In
        </Link>
      </div>

      <AuthFooter />
    </div>
  )
}
