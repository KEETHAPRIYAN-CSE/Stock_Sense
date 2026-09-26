import { createContext, useContext, useMemo, useState, type ReactNode } from 'react'
import type { User } from '../types'
import { authApi } from '../services/api'

type AuthContextValue = {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  loginWithGoogle: (payload: { email: string; full_name: string; google_id?: string; role?: string }) => Promise<void>
  register: (payload: { email: string; password: string; full_name: string; role: string }) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

function readUser(): User | null {
  const raw = localStorage.getItem('ss_user')
  if (!raw) return null
  try {
    return JSON.parse(raw) as User
  } catch {
    return null
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('ss_token'))
  const [user, setUser] = useState<User | null>(readUser)

  const persist = (nextToken: string, nextUser: User) => {
    localStorage.setItem('ss_token', nextToken)
    localStorage.setItem('ss_user', JSON.stringify(nextUser))
    setToken(nextToken)
    setUser(nextUser)
  }

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      token,
      login: async (email, password) => {
        const res = await authApi.login(email, password)
        persist(res.access_token, res.user)
      },
      loginWithGoogle: async (payload) => {
        const res = await authApi.google(payload)
        persist(res.access_token, res.user)
      },
      register: async (payload) => {
        const res = await authApi.register(payload)
        persist(res.access_token, res.user)
      },
      logout: () => {
        localStorage.removeItem('ss_token')
        localStorage.removeItem('ss_user')
        setToken(null)
        setUser(null)
        void authApi.logout().catch(() => undefined)
      },
    }),
    [token, user],
  )


  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('AuthProvider missing')
  return ctx
}
