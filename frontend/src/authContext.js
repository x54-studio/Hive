// src/AuthContext.js
import React, {
  createContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from 'react'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext()

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  const fetchUserProfile = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5000/api/protected', {
        method: 'GET',
        credentials: 'include',
      })
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else if (response.status === 401) {
        // Attempt token refresh if access token expired
        const refreshResponse = await fetch(
          'http://localhost:5000/api/refresh',
          {
            method: 'POST',
            credentials: 'include',
          }
        )
        if (refreshResponse.ok) {
          const retryResponse = await fetch(
            'http://localhost:5000/api/protected',
            {
              method: 'GET',
              credentials: 'include',
            }
          )
          if (retryResponse.ok) {
            const userData = await retryResponse.json()
            setUser(userData)
          } else {
            setUser(null)
          }
        } else {
          setUser(null)
        }
      } else {
        setUser(null)
      }
    } catch (error) {
      console.error('Error fetching profile:', error)
      setUser(null)
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        credentials: 'include',
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      setUser(null)
      localStorage.setItem('logout', Date.now().toString())
      navigate('/login')
    }
  }, [navigate])

  const login = useCallback(
    async (email, password) => {
      try {
        const response = await fetch('http://localhost:5000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
          credentials: 'include',
        })
        const data = await response.json()
        if (data.message === 'Login successful') {
          await fetchUserProfile()
          navigate('/profile')
        } else {
          throw new Error(data.message || 'Login failed')
        }
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    },
    [fetchUserProfile, navigate]
  )

  useEffect(() => {
    fetchUserProfile()
  }, [fetchUserProfile])

  useEffect(() => {
    const handleStorageLogout = (event) => {
      if (event.key === 'logout') {
        setUser(null)
        navigate('/login')
      }
    }
    window.addEventListener('storage', handleStorageLogout)
    return () => window.removeEventListener('storage', handleStorageLogout)
  }, [navigate])

  const contextValue = useMemo(
    () => ({ user, login, logout }),
    [user, login, logout]
  )

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  )
}

export { AuthContext, AuthProvider }
