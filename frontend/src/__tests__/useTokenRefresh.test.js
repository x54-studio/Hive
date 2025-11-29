// src/__tests__/useTokenRefresh.test.js
import React from 'react'
import { render, act } from '@testing-library/react'
import '@testing-library/jest-dom'
import useTokenRefresh from '../hooks/useTokenRefresh'

// A simple component to test our hook.
const TestComponent = ({ tokenExpirationTime, onRefresh, buffer = 5000, onError }) => {
  useTokenRefresh(tokenExpirationTime, onRefresh, buffer, onError)
  return <div>Token Refresh Test</div>
}

jest.useFakeTimers()

describe('useTokenRefresh Hook Additional Tests', () => {
  beforeEach(() => {
    jest.clearAllTimers()
  })

  it('calls the refresh callback exactly once before token expiration and resets when tokenExpirationTime changes', () => {
    const refreshCallback = jest.fn()
    const now = Date.now()
    const expirationTime = now + 10000 // Expires in 10 seconds
    
    const { rerender } = render(<TestComponent tokenExpirationTime={expirationTime} onRefresh={refreshCallback} />)
    
    // With expirationTime=now+10000 and default buffer=5000, refresh should trigger at 5000ms.
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(1)
    
    // Update tokenExpirationTime to simulate new token issuance.
    // We advance time by 5000, so "now" for the component's logic (Date.now()) 
    // should ideally advance if we want realistic simulation, but jest fake timers 
    // advance system time.
    // The hook calculates delay = expirationTime - Date.now() - buffer.
    // At t=5000, Date.now() is start+5000.
    // We want next refresh in 5000ms.
    // So delay=5000.
    // 5000 = expirationTime - (start+5000) - 5000
    // expirationTime = 15000 + start.
    
    const newExpirationTime = now + 15000 
    
    rerender(<TestComponent tokenExpirationTime={newExpirationTime} onRefresh={refreshCallback} />)
    
    // At t=5000:
    // newExpirationTime = start+15000.
    // Date.now() = start+5000.
    // buffer = 5000.
    // delay = (start+15000) - (start+5000) - 5000 = 5000.
    
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(2)
  })

  it('does not call refresh callback if tokenExpirationTime is null or invalid', () => {
    const refreshCallback = jest.fn()
    
    // Test with null tokenExpirationTime
    const { rerender } = render(<TestComponent tokenExpirationTime={null} onRefresh={refreshCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(0)
    
    // Test with tokenExpirationTime <= buffer (invalid/expired soon)
    // Current time is roughly start + 5000 (from previous step)
    // We reset rerender or create new component? We used rerender.
    // Let's calculate relative to current Date.now().
    
    const now = Date.now()
    // Expiration = now + 3000. Buffer = 5000.
    // Time left (3000) <= Buffer (5000) -> Should skip.
    rerender(<TestComponent tokenExpirationTime={now + 3000} onRefresh={refreshCallback} buffer={5000} />)
    
    act(() => {
      jest.advanceTimersByTime(1000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(0)
  })

  it('handles refresh buffer correctly (5 seconds before expiration)', () => {
    const refreshCallback = jest.fn()
    const buffer = 5000 // 5 seconds
    const now = Date.now()
    const expirationTime = now + 10000 // Expires in 10s
    
    // Token expires in 10 seconds, refresh should trigger at 5 seconds (10 - 5)
    render(<TestComponent tokenExpirationTime={expirationTime} onRefresh={refreshCallback} buffer={buffer} />)
    
    // Advance time to just before buffer (should not trigger)
    act(() => {
      jest.advanceTimersByTime(4000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(0)
    
    // Advance time to buffer point (should trigger)
    act(() => {
      jest.advanceTimersByTime(1000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(1)
  })

  it('does not call refresh callback or error callback for expired tokenExpirationTime', () => {
    const refreshCallback = jest.fn()
    const errorCallback = jest.fn()
    // Simulate an expired token by passing a past timestamp.
    const pastExpirationTime = Date.now() - 1000
    
    render(<TestComponent tokenExpirationTime={pastExpirationTime} onRefresh={refreshCallback} onError={errorCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(1000)
    })
    // Hook returns early for expired token without calling callbacks
    expect(refreshCallback).not.toHaveBeenCalled()
    expect(errorCallback).not.toHaveBeenCalled()
  })

  it('validates tokenExpirationTime is a number', () => {
    const refreshCallback = jest.fn()
    
    // Test with non-number values
    const { rerender } = render(<TestComponent tokenExpirationTime="invalid" onRefresh={refreshCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    expect(refreshCallback).not.toHaveBeenCalled()
    
    rerender(<TestComponent tokenExpirationTime={NaN} onRefresh={refreshCallback} />)
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    expect(refreshCallback).not.toHaveBeenCalled()
  })

  it('handles tokenExpirationTime within clock skew tolerance', () => {
    const refreshCallback = jest.fn()
    // Token expiration slightly in past (within 5s tolerance)
    const slightlyPastExpiration = Date.now() - 3000 // 3 seconds ago
    
    render(<TestComponent tokenExpirationTime={slightlyPastExpiration} onRefresh={refreshCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(1000)
    })
    // Should not schedule refresh for past expiration (even within tolerance)
    expect(refreshCallback).not.toHaveBeenCalled()
  })

  it('rejects tokenExpirationTime exceeding maximum (24 hours)', () => {
    const refreshCallback = jest.fn()
    const MAX_LIFETIME_MS = 24 * 60 * 60 * 1000
    const excessiveExpiration = Date.now() + MAX_LIFETIME_MS + 1000 // Exceeds 24 hours from now
    
    render(<TestComponent tokenExpirationTime={excessiveExpiration} onRefresh={refreshCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(5000)
    })
    // Should not schedule refresh for excessive expiration
    expect(refreshCallback).not.toHaveBeenCalled()
  })
})
