import { useEffect, useState, useRef, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { refresh, logout, refreshUser } from '../redux/slices/authSlice'
import useTokenRefresh from '../hooks/useTokenRefresh'
import axiosInstance from '../api/axiosInstance'
import { REFRESH_BUFFER_MS, STORAGE_KEYS, PERIODIC_CHECK_INTERVAL_MS, IS_DEVELOPMENT } from '../config'

const SessionManager = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)
  const userRef = useRef(user)
  const [tokenExpirationTime, setTokenExpirationTime] = useState(null)
  const loginTimeRef = useRef(null)

  // Keep userRef in sync with user state and track login time
  useEffect(() => {
    const prevUser = userRef.current
    userRef.current = user
    // Track when user is set (after login) - user changed from null/undefined to a value
    if (user && !prevUser) {
      loginTimeRef.current = Date.now()
      if (IS_DEVELOPMENT) {
        console.log("[SessionManager] User just logged in, setting grace period")
      }
    }
  }, [user])

  useEffect(() => {
    console.log("[SessionManager] ========================================")
    console.log("[SessionManager] useEffect triggered - checking authentication")
    console.log("[SessionManager] Current user state:", user ? "authenticated" : "not authenticated")
    console.log("[SessionManager] Current pathname:", window.location.pathname)
    
    // If no user in Redux state, no need to check
    if (!user) {
      console.log("[SessionManager] No user state, tokenExpirationTime set to null (expected for unauthenticated)")
      setTokenExpirationTime(null)
      loginTimeRef.current = null
      return
    }
    
    // Grace period after login: skip verification for 5 seconds to allow cookies to be processed
    const timeSinceLogin = loginTimeRef.current ? Date.now() - loginTimeRef.current : Infinity
    const GRACE_PERIOD_MS = 5000 // 5 seconds
    
    if (timeSinceLogin < GRACE_PERIOD_MS) {
      console.log(`[SessionManager] Within grace period after login (${timeSinceLogin}ms < ${GRACE_PERIOD_MS}ms), skipping verification`)
      // Use token expiration from login response if available
      if (user?.claims?.exp) {
        const expTime = user.claims.exp * 1000
        if (expTime > Date.now()) {
          setTokenExpirationTime(expTime)
          console.log("[SessionManager] Using token expiration from login response:", new Date(expTime).toLocaleTimeString())
        }
      } else {
        // Fallback: use default 15 minutes from now
        setTokenExpirationTime(Date.now() + 15 * 60 * 1000)
      }
      return
    }
  }, [user])

  const checkTokenExpiration = useCallback(async () => {
    if (IS_DEVELOPMENT) {
      console.log("[SessionManager] checkTokenExpiration() called")
    }
    
    try {
      const response = await axiosInstance.get('/protected', { withCredentials: true })
      
      const claims = response.data?.claims
      if (claims?.exp) {
        // Token lifetime validation: ensure exp is valid
        if (typeof claims.exp !== 'number' || claims.exp <= 0) {
          console.error("[SessionManager] Invalid exp claim:", claims.exp)
          dispatch(logout())
          setTokenExpirationTime(null)
          setTimeout(() => {
            if (window.location.pathname !== '/login') {
              navigate('/login', { replace: true })
            }
          }, 100)
          return false
        }

        const expTime = claims.exp * 1000
        const lifetime = expTime - Date.now()
        
        if (IS_DEVELOPMENT) {
          const lifetimeMinutes = Math.floor(lifetime / 60000)
          const lifetimeSeconds = Math.floor((lifetime % 60000) / 1000)
          console.log("[SessionManager] Token expires at:", new Date(expTime).toLocaleTimeString(), "(in", lifetimeMinutes, "min", lifetimeSeconds, "sec)")
        }
        
        // Handle clock skew: accept tokens expiring up to 5 seconds in the past
        const CLOCK_SKEW_TOLERANCE_MS = 5000
        if (lifetime < -CLOCK_SKEW_TOLERANCE_MS) {
          console.warn("[SessionManager] Token expired (lifetime:", lifetime, "ms), logging out")
          dispatch(logout())
          setTokenExpirationTime(null)
          setTimeout(() => {
            if (window.location.pathname !== '/login') {
              navigate('/login', { replace: true })
            }
          }, 100)
          return false
        }
        
        // Bounds checking: reject lifetimes > 24 hours (likely calculation error)
        const MAX_LIFETIME_MS = 24 * 60 * 60 * 1000 // 24 hours
        if (lifetime > MAX_LIFETIME_MS) {
          console.error("[SessionManager] Token lifetime exceeds maximum (", lifetime, "ms > ", MAX_LIFETIME_MS, "ms), using default")
          const defaultExp = Date.now() + 15 * 60 * 1000
          setTokenExpirationTime(defaultExp)
          return true
        }
        
        // Update expiration time - state update will be ignored if value hasn't changed
        setTokenExpirationTime(expTime)
        if (IS_DEVELOPMENT) {
          console.log("[SessionManager] tokenExpirationTime state updated (or kept same)")
        }
        return true
      } else {
        console.warn("[SessionManager] No exp in response, using default 15 minutes")
        const defaultExp = Date.now() + 15 * 60 * 1000
        setTokenExpirationTime(defaultExp)
        return true
      }
    } catch (error) {
      console.error("[SessionManager] Backend verification failed:", error.response?.status, error.response?.data)
      if (error.response?.status === 401) {
        console.warn("[SessionManager] Token invalid or expired, logging out")
        dispatch(logout())
        setTokenExpirationTime(null)
        setTimeout(() => {
          if (window.location.pathname !== '/login') {
            navigate('/login', { replace: true })
          }
        }, 100)
      }
      return false
    }
  }, [dispatch, navigate])

  // Check token on mount and set up periodic checks
  useEffect(() => {
    if (!user) {
      setTokenExpirationTime(null)
      loginTimeRef.current = null
      return
    }

    // Check token on mount
    console.log("[SessionManager] Calling checkTokenExpiration() on mount...")
    checkTokenExpiration().then((isValid) => {
      console.log("[SessionManager] checkTokenExpiration() returned:", isValid)
      console.log("[SessionManager] ========================================")
    })
    
    // Set up periodic check as fallback safety net (only if proactive refresh fails silently)
    // Reduced frequency since proactive refresh handles most cases
    if (IS_DEVELOPMENT) {
      console.log(`[SessionManager] Setting up periodic token expiration check (every ${PERIODIC_CHECK_INTERVAL_MS / 1000}s - fallback safety net)`)
    }
    const expirationCheckInterval = setInterval(() => {
      if (!userRef.current) {
        if (IS_DEVELOPMENT) {
          console.log("[SessionManager] No user state, clearing interval")
        }
        clearInterval(expirationCheckInterval)
        return
      }
      if (IS_DEVELOPMENT) {
        console.log("[SessionManager] Running periodic token expiration check (fallback safety net)...")
      }
      checkTokenExpiration()
    }, PERIODIC_CHECK_INTERVAL_MS)

    return () => {
      clearInterval(expirationCheckInterval)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]) // Removed checkTokenExpiration from deps to avoid infinite loops/race conditions

  const refreshCallback = useCallback(async (skipMultiTabCheck = false) => {
    if (IS_DEVELOPMENT) {
      console.log("[SessionManager] refreshCallback called - starting token refresh")
    }
    
    // Check if we're still within grace period (cookies might not be available yet)
    // This check should happen BEFORE setting locks to avoid unnecessary lock operations
    const timeSinceLogin = loginTimeRef.current ? Date.now() - loginTimeRef.current : Infinity
    const GRACE_PERIOD_MS = 5000
    
    if (timeSinceLogin < GRACE_PERIOD_MS && !skipMultiTabCheck) {
      if (IS_DEVELOPMENT) {
        console.log(`[SessionManager] Still within grace period (${timeSinceLogin}ms < ${GRACE_PERIOD_MS}ms), skipping refresh attempt`)
      }
      
      // Schedule a retry for after the grace period
      const timeUntilGraceEnds = GRACE_PERIOD_MS - timeSinceLogin
      if (IS_DEVELOPMENT) {
        console.log(`[SessionManager] Scheduling retry after grace period in ${timeUntilGraceEnds + 500}ms`)
      }
      setTimeout(() => {
        if (userRef.current) {
          refreshCallback(true) // skipMultiTabCheck=true
        }
      }, timeUntilGraceEnds + 500)
      
      return
    }
    
    // Multi-tab coordination: Check if another tab is already refreshing
    if (!skipMultiTabCheck) {
      const refreshLock = localStorage.getItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
      if (refreshLock) {
        const lockTime = parseInt(refreshLock, 10)
        const lockAge = Date.now() - lockTime
        // If lock is recent (< 10 seconds), another tab is handling refresh
        if (lockAge < 10000) {
          if (IS_DEVELOPMENT) {
            console.log("[SessionManager] Another tab is refreshing, skipping duplicate request")
          }
          return
        }
        // Lock is stale, remove it
        localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
      }
      
      // Set lock before refresh
      localStorage.setItem(STORAGE_KEYS.REFRESH_IN_PROGRESS, Date.now().toString())
    }
    
    if (IS_DEVELOPMENT) {
      console.log("[SessionManager] Attempting token refresh...")
    }
    
    // Network failure handling with exponential backoff retry
    const MAX_RETRIES = 3
    const RETRY_DELAYS = [1000, 2000, 4000] // Exponential backoff: 1s, 2s, 4s
    
    let lastError = null
    
    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      try {
        const refreshResult = await dispatch(refresh())
        
        console.log("[SessionManager] Refresh result:", refresh.fulfilled.match(refreshResult) ? "SUCCESS" : "FAILED")
        
        if (refresh.fulfilled.match(refreshResult)) {
          console.log("[SessionManager] Refresh successful, extracting exp from response...")
          const refreshData = refreshResult.payload
          const claims = refreshData?.claims
          
          if (claims?.exp) {
            // Token lifetime validation
            if (typeof claims.exp !== 'number' || claims.exp <= 0) {
              console.error("[SessionManager] Invalid exp claim in refresh response:", claims.exp)
              localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
              dispatch(logout())
              setTimeout(() => {
                if (window.location.pathname !== '/login') {
                  navigate('/login', { replace: true })
                }
              }, 100)
              return
            }

            const newLifetime = claims.exp * 1000 - Date.now()
            
            // Handle clock skew: accept tokens expiring up to 5 seconds in the past
            const CLOCK_SKEW_TOLERANCE_MS = 5000
            if (newLifetime < -CLOCK_SKEW_TOLERANCE_MS) {
              console.error("[SessionManager] Refreshed token already expired (lifetime:", newLifetime, "ms)")
              localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
              dispatch(logout())
              setTimeout(() => {
                if (window.location.pathname !== '/login') {
                  navigate('/login', { replace: true })
                }
              }, 100)
              return
            }
            
            // Bounds checking: reject lifetimes > 24 hours
            const MAX_LIFETIME_MS = 24 * 60 * 60 * 1000
            if (newLifetime > MAX_LIFETIME_MS) {
              console.error("[SessionManager] Refreshed token lifetime exceeds maximum, using default")
              setTokenExpirationTime(Date.now() + 15 * 60 * 1000)
            } else {
              const newExpTime = claims.exp * 1000
              const newLifetimeMinutes = Math.floor(newLifetime / 60000)
              const newLifetimeSeconds = Math.floor((newLifetime % 60000) / 1000)
              console.log("[SessionManager] New token expires at:", new Date(newExpTime).toLocaleTimeString(), "(in", newLifetimeMinutes, "min", newLifetimeSeconds, "sec)")
              
              setTokenExpirationTime(newExpTime)
            }
            
            // Broadcast refresh success to other tabs
            localStorage.setItem(STORAGE_KEYS.TOKEN_REFRESHED, JSON.stringify({
              timestamp: Date.now(),
              username: refreshData.username,
              claims: claims
            }))
          } else {
            console.warn("[SessionManager] No exp in refresh response, using default 15 minutes")
            setTokenExpirationTime(Date.now() + 15 * 60 * 1000)
          }
          
          // Remove lock after successful refresh
          localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
          return // Success, exit retry loop
        } else {
          // Refresh failed - check error type
          const errorData = refreshResult.payload
          lastError = errorData
          
          // Check if it's an auth error (401/403) - logout immediately, no retry
          if (errorData?.error && (errorData.error.includes('Unauthorized') || errorData.error.includes('Invalid'))) {
            console.warn("[SessionManager] Auth error during refresh, logging out (no retry)")
            localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
            dispatch(logout())
            setTimeout(() => {
              if (window.location.pathname !== '/login') {
                navigate('/login', { replace: true })
              }
            }, 100)
            return // Auth error, exit retry loop
          }
          
          // For non-auth errors, continue to retry logic below
        }
      } catch (error) {
        lastError = error
        
        // Check if it's a network error (not auth error)
        const isNetworkError = !error.response || 
                               error.code === 'ECONNABORTED' || 
                               error.code === 'ERR_NETWORK' ||
                               error.message?.includes('Network Error')
        
        if (!isNetworkError) {
          // Not a network error, check if it's auth error
          if (error.response?.status === 401 || error.response?.status === 403) {
            console.warn("[SessionManager] Auth error during refresh, logging out (no retry)")
            localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
            dispatch(logout())
            setTimeout(() => {
              if (window.location.pathname !== '/login') {
                navigate('/login', { replace: true })
              }
            }, 100)
            return // Auth error, exit retry loop
          }
        }
        
        // Network error or other non-auth error - retry if attempts remaining
        if (attempt < MAX_RETRIES) {
          const delay = RETRY_DELAYS[attempt]
          console.warn(`[SessionManager] Refresh attempt ${attempt + 1} failed (network error), retrying in ${delay}ms...`)
          await new Promise(resolve => setTimeout(resolve, delay))
          continue // Retry
        } else {
          // All retries exhausted
          console.error("[SessionManager] Refresh failed after", MAX_RETRIES + 1, "attempts, logging out")
          localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
          dispatch(logout())
          setTimeout(() => {
            if (window.location.pathname !== '/login') {
              navigate('/login', { replace: true })
            }
          }, 100)
          return // All retries failed, exit
        }
      }
    }
    
    // If we get here, all retries failed (shouldn't happen due to returns above, but safety check)
    console.error("[SessionManager] Refresh failed after all retries")
    localStorage.removeItem(STORAGE_KEYS.REFRESH_IN_PROGRESS)
    dispatch(logout())
    setTimeout(() => {
      if (window.location.pathname !== '/login') {
        navigate('/login', { replace: true })
      }
    }, 100)
    
    console.log("[SessionManager] ========================================")
  }, [dispatch, navigate, user])

  useTokenRefresh(tokenExpirationTime, refreshCallback, REFRESH_BUFFER_MS, (error) => {
    console.error("useTokenRefresh error:", error)
  })

  // Page Visibility API: Handle tab visibility changes and app return from inactive state
  useEffect(() => {
    if (!user) return

    const handleVisibilityChange = async () => {
      if (document.visibilityState === 'visible') {
        console.log("[SessionManager] Tab became visible, checking token status...")
        const isValid = await checkTokenExpiration()
        
        if (isValid) {
          // Token is valid, but check if we need immediate refresh
          // Get current lifetime from user claims or state
          const currentClaims = user?.claims
          const expTime = currentClaims?.exp ? currentClaims.exp * 1000 : tokenExpirationTime
          
          if (expTime) {
            const timeLeft = expTime - Date.now()
            if (timeLeft < REFRESH_BUFFER_MS) {
              console.log("[SessionManager] Token expires soon (< buffer), triggering immediate refresh")
              refreshCallback(true) // Skip multi-tab check for visibility-triggered refresh
            } else {
              // Reschedule if needed (state update ignored if same value)
              setTokenExpirationTime(expTime)
            }
          }
        }
        // If invalid, checkTokenExpiration already handles logout
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange)
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [user, tokenExpirationTime, refreshCallback, checkTokenExpiration])

  // Multi-tab coordination: Listen for token refresh from other tabs
  useEffect(() => {
    if (!user) return

    const handleStorageChange = (e) => {
      if (e.key === STORAGE_KEYS.TOKEN_REFRESHED && e.newValue) {
        try {
          const refreshData = JSON.parse(e.newValue)
          const claims = refreshData.claims
          
          if (claims?.exp) {
            const newExpTime = claims.exp * 1000
            if (newExpTime > Date.now()) {
              if (IS_DEVELOPMENT) {
                console.log("[SessionManager] Token refreshed by another tab, updating state")
              }
              // Update Redux state with new token data
              dispatch(refreshUser.fulfilled({
                username: refreshData.username || user.username,
                claims: claims
              }))
              setTokenExpirationTime(newExpTime)
            }
          }
        } catch (error) {
          console.error("[SessionManager] Error parsing storage event:", error)
        }
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => {
      window.removeEventListener('storage', handleStorageChange)
    }
  }, [user, dispatch])

  // Focus event handling: re-validate token when tab regains focus
  useEffect(() => {
    if (!user) return

    const handleFocus = async () => {
      if (IS_DEVELOPMENT) {
        console.log("[SessionManager] Tab gained focus, re-checking token status...")
      }
      await checkTokenExpiration()
    }

    window.addEventListener('focus', handleFocus)
    return () => {
      window.removeEventListener('focus', handleFocus)
    }
  }, [user, checkTokenExpiration])

  // This component is used only for background session management.
  return null
}

export default SessionManager
