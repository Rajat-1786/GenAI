import { useState } from 'react'
import SocialButtons from './SocialButtons.jsx'
import { signup } from '../api.js'
import './AuthPage.css'

const EMPTY = { name: '', email: '', password: '', confirm: '' }

function validate(mode, values) {
  const errors = {}
  if (mode === 'signup' && !values.name.trim()) errors.name = 'Please tell us your name.'
  if (!/^\S+@\S+\.\S+$/.test(values.email)) errors.email = 'Enter a valid email address.'
  if (values.password.length < 8) errors.password = 'Use at least 8 characters.'
  if (mode === 'signup' && values.confirm !== values.password) {
    errors.confirm = 'Passwords do not match.'
  }
  return errors
}

function Field({ id, label, error, ...props }) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input id={id} name={id} aria-invalid={!!error} {...props} />
      {error && <span className="field-error">{error}</span>}
    </div>
  )
}

export default function AuthPage() {
  const [mode, setMode] = useState('login')
  const [values, setValues] = useState(EMPTY)
  const [errors, setErrors] = useState({})
  const [showPassword, setShowPassword] = useState(false)
  const [done, setDone] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [apiError, setApiError] = useState('')

  const isSignup = mode === 'signup'

  const switchMode = (next) => {
    setMode(next)
    setErrors({})
    setApiError('')
    setDone(false)
  }

  const onChange = (e) => {
    setValues((v) => ({ ...v, [e.target.name]: e.target.value }))
    setErrors((er) => ({ ...er, [e.target.name]: undefined }))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    const found = validate(mode, values)
    setErrors(found)
    setApiError('')
    if (Object.keys(found).length > 0) return

    if (!isSignup) {
      // TODO: call /auth/login once the backend accepts credentials.
      setDone(true)
      return
    }

    setSubmitting(true)
    try {
      await signup(values)
      setDone(true)
      setValues(EMPTY)
    } catch (err) {
      setApiError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  const onSocial = (provider) => {
    // TODO: redirect to the backend OAuth route, e.g. /auth/{provider}/login.
    console.log('Social login requested:', provider)
  }

  return (
    <main className="auth">
      <section className="auth-hero" aria-hidden="true">
        <div className="orb orb-a" />
        <div className="orb orb-b" />
        <div className="hero-content">
          <span className="brand">AiChat</span>
          <h1>
            Conversations with <em>intention</em>.
          </h1>
          <p>
            A calm place to think out loud, ask better questions, and let the
            answers arrive with clarity.
          </p>
        </div>
        <span className="hero-foot">Your moment, preserved.</span>
      </section>

      <section className="auth-panel">
        <div className="card">
          <div className="tabs" role="tablist">
            <button
              role="tab"
              aria-selected={!isSignup}
              className={!isSignup ? 'active' : ''}
              onClick={() => switchMode('login')}
              type="button"
            >
              Log in
            </button>
            <button
              role="tab"
              aria-selected={isSignup}
              className={isSignup ? 'active' : ''}
              onClick={() => switchMode('signup')}
              type="button"
            >
              Sign up
            </button>
          </div>

          <h2>{isSignup ? 'Create your account' : 'Welcome back'}</h2>
          <p className="subtitle">
            {isSignup
              ? 'Begin with a few details and step into the conversation.'
              : 'Sign in to pick up where you left off.'}
          </p>

          {done ? (
            <div className="success" role="status">
              {isSignup ? 'Your account is ready.' : 'You are signed in.'}
            </div>
          ) : (
            <form onSubmit={onSubmit} noValidate>
              {isSignup && (
                <Field
                  id="name"
                  label="Full name"
                  autoComplete="name"
                  placeholder="Your name"
                  value={values.name}
                  onChange={onChange}
                  error={errors.name}
                />
              )}
              <Field
                id="email"
                label="Email"
                type="email"
                autoComplete="email"
                placeholder="you@example.com"
                value={values.email}
                onChange={onChange}
                error={errors.email}
              />
              <div className="password-wrap">
                <Field
                  id="password"
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete={isSignup ? 'new-password' : 'current-password'}
                  placeholder="At least 8 characters"
                  value={values.password}
                  onChange={onChange}
                  error={errors.password}
                />
                <button
                  type="button"
                  className="toggle-pw"
                  onClick={() => setShowPassword((s) => !s)}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
              {isSignup && (
                <Field
                  id="confirm"
                  label="Confirm password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  placeholder="Repeat your password"
                  value={values.confirm}
                  onChange={onChange}
                  error={errors.confirm}
                />
              )}

              {!isSignup && (
                <a className="forgot" href="#forgot">
                  Forgot password?
                </a>
              )}

              {apiError && (
                <div className="form-error" role="alert">
                  {apiError}
                </div>
              )}

              <button type="submit" className="submit" disabled={submitting}>
                {submitting
                  ? 'Please wait…'
                  : isSignup
                    ? 'Create account'
                    : 'Log in'}
              </button>
            </form>
          )}

          {!done && <SocialButtons onSelect={onSocial} />}

          <p className="switch">
            {isSignup ? 'Already have an account?' : 'New to AiChat?'}{' '}
            <button
              type="button"
              onClick={() => switchMode(isSignup ? 'login' : 'signup')}
            >
              {isSignup ? 'Log in' : 'Create an account'}
            </button>
          </p>
        </div>
      </section>
    </main>
  )
}
