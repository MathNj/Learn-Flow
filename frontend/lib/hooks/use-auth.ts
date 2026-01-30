'use client'

import { useEffect } from 'react'
import { useAuthStore } from '@/lib/stores/auth-store'
import api from '@/lib/api'

export function useAuth() {
  const { user, token, isAuthenticated, setAuth, clearAuth, updateUser } = useAuthStore()

  useEffect(() => {
    // Verify token on mount
    if (token && !user) {
      api
        .getCurrentUser()
        .then((fetchedUser) => {
          setAuth(fetchedUser, token)
        })
        .catch(() => {
          clearAuth()
        })
    }
  }, [token, user, setAuth, clearAuth])

  const login = async (email: string, password: string) => {
    const data = await api.login(email, password)
    setAuth(data.user, data.token)
    return data
  }

  const register = async (data: {
    username: string
    email: string
    password: string
    role: 'student' | 'teacher'
  }) => {
    const result = await api.register(data)
    setAuth(result.user, result.token)
    return result
  }

  const logout = () => {
    api.logout()
    clearAuth()
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
  }
}
