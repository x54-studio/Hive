// src/__tests__/useTokenRefresh.test.js
import React from 'react'
import { render, act } from '@testing-library/react'
import '@testing-library/jest-dom'
import useTokenRefresh from '../hooks/useTokenRefresh'

// A simple component to test our hook.
const TestComponent = ({ tokenLifetime, onRefresh, buffer = 1000, onError }) => {
  useTokenRefresh(tokenLifetime, onRefresh, buffer, onError)
  return <div>Token Refresh Test</div>
}

jest.useFakeTimers()

describe('useTokenRefresh Hook Additional Tests', () => {
  beforeEach(() => {
    // Ensure the multi‑tab flag is cleared before each test.
    localStorage.removeItem('refreshInProgress')
  })

  it('calls the refresh callback exactly once before token expiration and resets when tokenLifetime changes', () => {
    const refreshCallback = jest.fn()
    const { rerender } = render(<TestComponent tokenLifetime={3000} onRefresh={refreshCallback} />)
    
    // With tokenLifetime=3000 and default buffer=1000, refresh should trigger at 2000ms.
    act(() => {
      jest.advanceTimersByTime(2000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(1)
    
    // Update tokenLifetime to simulate new token issuance.
    rerender(<TestComponent tokenLifetime={5000} onRefresh={refreshCallback} />)
    
    // With new tokenLifetime=5000, refresh should trigger after 5000-1000 = 4000ms.
    act(() => {
      jest.advanceTimersByTime(4000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(2)
  })

  it('does not call refresh callback if multi-tab flag is set', () => {
    const refreshCallback = jest.fn()
    localStorage.setItem('refreshInProgress', 'true')
    const tokenLifetime = 3000
    
    render(<TestComponent tokenLifetime={tokenLifetime} onRefresh={refreshCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(3000)
    })
    expect(refreshCallback).toHaveBeenCalledTimes(0)
    
    // Clean up the flag.
    localStorage.removeItem('refreshInProgress')
  })

  it('calls the error callback if refresh fails due to invalid tokenLifetime', () => {
    const refreshCallback = jest.fn()
    const errorCallback = jest.fn()
    // Simulate an invalid token lifetime by passing a negative value.
    const invalidTokenLifetime = -1000
    
    render(<TestComponent tokenLifetime={invalidTokenLifetime} onRefresh={refreshCallback} onError={errorCallback} />)
    
    act(() => {
      jest.advanceTimersByTime(1000)
    })
    expect(refreshCallback).not.toHaveBeenCalled()
    expect(errorCallback).toHaveBeenCalled()
  })
})
