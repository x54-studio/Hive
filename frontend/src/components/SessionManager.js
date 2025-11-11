import { useEffect, useState } from 'react'
import { useDispatch } from 'react-redux'
import { jwtDecode } from 'jwt-decode'
import { refresh, logout } from '../redux/slices/authSlice'
import useTokenRefresh from '../hooks/useTokenRefresh'

// Helper function to read a cookie by name.
const getCookie = (name) => {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? match[2] : null
}

const SessionManager = () => {
  const dispatch = useDispatch()
  const [tokenLifetime, setTokenLifetime] = useState(null)

  useEffect(() => {
    // Retrieve the access token from cookies.
    const accessToken = getCookie('access_token')
    if (!accessToken) {
      // No token is normal for unauthenticated users - no action needed
      return
    }
    try {
      const decoded = jwtDecode(accessToken)
      // Compute lifetime: decoded.exp is in seconds, so multiply by 1000.
      const lifetime = decoded.exp * 1000 - Date.now()
      console.log("Computed tokenLifetime:", lifetime)
      setTokenLifetime(lifetime)
    } catch (error) {
      console.error("Error decoding token:", error)
      dispatch(logout())
    }
  }, [dispatch])

  const refreshCallback = async () => {
    console.log("Refreshing token...")
    await dispatch(refresh())
    // After refreshing, read and decode the new token from cookies.
    const newAccessToken = getCookie('access_token')
    if (newAccessToken) {
      try {
        const decoded = jwtDecode(newAccessToken)
        const newLifetime = decoded.exp * 1000 - Date.now()
        console.log("New token lifetime:", newLifetime)
        setTokenLifetime(newLifetime)
      } catch (error) {
        console.error("Error decoding new token:", error)
      }
    } else {
      console.warn("No new access token found after refresh.")
      dispatch(logout())
    }
  }

  useTokenRefresh(tokenLifetime, refreshCallback, 1000, (error) => {
    console.error("useTokenRefresh error:", error)
  })

  // This component is used only for background session management.
  return null
}

export default SessionManager
