import { useEffect, useRef } from 'react'

/**
 * Custom hook to automatically refresh an access token.
 *
 * @param {number} tokenLifetime - The lifetime of the token in milliseconds.
 * @param {Function} refreshCallback - The function to call to refresh the token.
 * @param {number} buffer - Time in milliseconds to subtract from tokenLifetime (default is 1000ms).
 * @param {Function} onError - Optional callback for handling errors.
 */
const useTokenRefresh = (tokenLifetime, refreshCallback, buffer = 1000, onError) => {
  const refreshTimeout = useRef(null)

  useEffect(() => {
    // Clear any existing timer when dependencies change.
    if (refreshTimeout.current) {
      clearTimeout(refreshTimeout.current)
      refreshTimeout.current = null
    }

    // If tokenLifetime is null or not a positive number, log a warning and do nothing.
    if (tokenLifetime == null || tokenLifetime <= buffer) {
      console.warn(`useTokenRefresh: tokenLifetime is invalid (${tokenLifetime}). No timer scheduled.`)
      if (onError) onError(new Error(`Invalid token lifetime: ${tokenLifetime} (buffer: ${buffer})`))
      return
    }

    console.log("useTokenRefresh: tokenLifetime =", tokenLifetime, "buffer =", buffer)
    const delay = tokenLifetime - buffer
    console.log("Setting token refresh timer with delay:", delay, "ms")

    refreshTimeout.current = setTimeout(() => {
      console.log("Token refresh timer triggered. Calling refresh callback.")
      refreshCallback()
      // Clear the timeout reference so that a new timer can be scheduled after refresh.
      refreshTimeout.current = null
    }, delay)

    return () => {
      if (refreshTimeout.current) {
        clearTimeout(refreshTimeout.current)
        refreshTimeout.current = null
      }
    }
  }, [tokenLifetime, refreshCallback, buffer, onError])
}

export default useTokenRefresh
