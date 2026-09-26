import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, X, Check, User as UserIcon } from 'lucide-react'
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

function GoogleLogo() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24">
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
        gap: 12,
        padding: '12px 18px',
        fontWeight: 600,
        backgroundColor: '#ffffff',
        borderColor: '#d5cec0',
        color: '#282421',
      }}
      onClick={onClick}
    >
      <GoogleLogo />
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

interface GoogleAuthModalProps {
  isOpen: boolean
  onClose: () => void
  onSelectAccount: (email: string, fullName: string) => Promise<void>
  busy: boolean
  error?: string
}

function GoogleAuthModal({ isOpen, onClose, onSelectAccount, busy, error }: GoogleAuthModalProps) {
  const [customEmail, setCustomEmail] = useState('')
  const [isCustom, setIsCustom] = useState(false)

  if (!isOpen) return null

  const defaultAccount = {
    email: 'keethapriyan.71382402066@sritcbe.ac.in',
    name: 'Keethapriyan',
    pictureLetter: 'K',
  }

  const handleCustomSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!customEmail.trim()) return
    const name = customEmail.split('@')[0]
    onSelectAccount(customEmail.trim(), name)
  }

  return (
    <div className="modal-overlay" style={{ zIndex: 1000 }}>
      <div className="modal" style={{ maxWidth: 460, padding: 32, borderRadius: 16 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 20 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <GoogleLogo />
            <div>
              <h2 style={{ fontSize: 18, fontWeight: 700, margin: 0, color: 'var(--text-title)' }}>Sign in with Google</h2>
              <p style={{ fontSize: 12.5, color: 'var(--text-muted)', margin: '2px 0 0' }}>Choose an account to continue to StockSense</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={busy}
            style={{ background: 'none', border: 0, cursor: 'pointer', color: 'var(--text-muted)', padding: 4 }}
          >
            <X size={20} />
          </button>
        </div>

        {error ? <div className="alert" style={{ marginBottom: 16 }}>{error}</div> : null}

        {!isCustom ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {/* Primary Google Account Card */}
            <div
              onClick={() => !busy && onSelectAccount(defaultAccount.email, defaultAccount.name)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 14,
                padding: '14px 16px',
                border: '1.5px solid #ded7c6',
                borderRadius: 12,
                cursor: busy ? 'not-allowed' : 'pointer',
                background: '#faf8f5',
                transition: 'all 0.15s ease',
              }}
              onMouseEnter={(e) => {
                if (!busy) e.currentTarget.style.backgroundColor = '#f3eee4'
              }}
              onMouseLeave={(e) => {
                if (!busy) e.currentTarget.style.backgroundColor = '#faf8f5'
              }}
            >
              <div
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #1d7468, #15803d)',
                  color: '#fff',
                  display: 'grid',
                  placeItems: 'center',
                  fontWeight: 700,
                  fontSize: 16,
                }}
              >
                {defaultAccount.pictureLetter}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <strong style={{ display: 'block', fontSize: 14, color: 'var(--text-dark)' }}>{defaultAccount.name}</strong>
                <span style={{ display: 'block', fontSize: 12.5, color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {defaultAccount.email}
                </span>
              </div>
              <Check size={18} color="var(--ok)" />
            </div>

            {/* Quick 1-Click Action */}
            <button
              type="button"
              className="btn"
              disabled={busy}
              onClick={() => onSelectAccount(defaultAccount.email, defaultAccount.name)}
              style={{ width: '100%', padding: '12px', marginTop: 4 }}
            >
              {busy ? 'Authenticating with Google…' : `Continue as ${defaultAccount.name}`}
            </button>

            <button
              type="button"
              className="btn secondary"
              disabled={busy}
              onClick={() => setIsCustom(true)}
              style={{ width: '100%', padding: '10px', fontSize: 13.5 }}
            >
              <UserIcon size={16} /> Use another Google account
            </button>
          </div>
        ) : (
          <form onSubmit={handleCustomSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <label style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-muted)' }}>
              Enter your Google / Gmail Email:
              <input
                type="email"
                placeholder="name@gmail.com"
                value={customEmail}
                onChange={(e) => setCustomEmail(e.target.value)}
                autoFocus
                required
                style={{ width: '100%', marginTop: 6 }}
              />
            </label>
            <div style={{ display: 'flex', gap: 10, marginTop: 6 }}>
              <button
                type="button"
                className="btn secondary"
                onClick={() => setIsCustom(false)}
                disabled={busy}
                style={{ flex: 1 }}
              >
                Back
              </button>
              <button
                type="submit"
                className="btn"
                disabled={busy || !customEmail.trim()}
                style={{ flex: 2 }}
              >
                {busy ? 'Signing in…' : 'Sign in'}
              </button>
            </div>
          </form>
        )}

        <div style={{ marginTop: 20, paddingTop: 16, borderTop: '1px solid #ede8de', textAlign: 'center' }}>
          <p style={{ fontSize: 11.5, color: 'var(--text-dim)', margin: 0 }}>
            To continue, Google will share your name and email address with StockSense.
          </p>
        </div>
      </div>
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
  const [showGoogleModal, setShowGoogleModal] = useState(false)

  const onGoogleAccountSelected = async (googleEmail: string, fullName: string) => {
    setBusy(true)
    setError('')
    try {
      await loginWithGoogle({
        email: googleEmail,
        full_name: fullName,
      })
      setShowGoogleModal(false)
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

        <GoogleButton onClick={() => setShowGoogleModal(true)} label="Sign in with Google" />
      </div>

      {/* Secondary Card: Don't have an account? */}
      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Don't have a StockSense Account?</h2>
        <Link to="/register" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Create Account
        </Link>
      </div>

      <AuthFooter />

      {/* Google Sign In Modal */}
      <GoogleAuthModal
        isOpen={showGoogleModal}
        onClose={() => setShowGoogleModal(false)}
        onSelectAccount={onGoogleAccountSelected}
        busy={busy}
        error={error}
      />
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
  const [showGoogleModal, setShowGoogleModal] = useState(false)

  const onGoogleAccountSelected = async (googleEmail: string, name: string) => {
    setBusy(true)
    setError('')
    try {
      await loginWithGoogle({
        email: googleEmail,
        full_name: name,
        role: role,
      })
      setShowGoogleModal(false)
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

        <GoogleButton onClick={() => setShowGoogleModal(true)} label="Sign up with Google" />
      </div>

      <div className="auth-card secondary-card">
        <h2 className="secondary-title">Already have a StockSense Account?</h2>
        <Link to="/login" className="btn secondary" style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
          Sign In
        </Link>
      </div>

      <AuthFooter />

      {/* Google Sign In Modal */}
      <GoogleAuthModal
        isOpen={showGoogleModal}
        onClose={() => setShowGoogleModal(false)}
        onSelectAccount={onGoogleAccountSelected}
        busy={busy}
        error={error}
      />
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
