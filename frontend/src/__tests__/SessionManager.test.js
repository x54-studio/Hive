// src/__tests__/SessionManager.test.js

import React from 'react'
import { render, act, waitFor } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import SessionManager from '../components/SessionManager'
import authReducer, { refresh, logout } from '../redux/slices/authSlice'

// Use fake timers for scheduling refresh callbacks.
jest.useFakeTimers()

// Mock jwt-decode so that when called it returns an object with an exp claim.
// Here, we simulate a token that will expire in 6000 ms (6 seconds) from now.
import { jwtDecode } from 'jwt-decode'
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn(() => ({
    exp: Math.floor((Date.now() + 6000) / 1000) // exp in seconds
  }))
}))

describe('SessionManager', () => {
  let store

  beforeEach(() => {
    // Create a Redux store with the auth reducer.
    store = configureStore({
      reducer: { auth: authReducer }
    })
    // Override dispatch to be a mock so we can inspect calls.
    store.dispatch = jest.fn(() => Promise.resolve({ payload: {} }))
    // Set a dummy access token cookie.
    document.cookie = "access_token=dummyTokenValue"
  })

  afterEach(() => {
    jest.clearAllTimers()
  })

  test('initializes session and schedules auto-refresh', async () => {
    // Render SessionManager (a background component that sets up auto-refresh).
    render(
      <Provider store={store}>
        <SessionManager />
      </Provider>
    )

    // The token lifetime should be computed from the decoded token.
    // With a token lifetime of ~6000ms and a buffer of 1000ms,
    // the refresh should be scheduled to fire after 5000ms.
    act(() => {
      jest.advanceTimersByTime(5000)
    })

    // Wait for the refresh thunk to be dispatched.
    await waitFor(() => {
      expect(store.dispatch).toHaveBeenCalledWith(refresh())
    })
  })

  test('does not schedule auto-refresh when no access token is present', async () => {
    // Clear the cookie to simulate no token.
    document.cookie = ""
    render(
      <Provider store={store}>
        <SessionManager />
      </Provider>
    )
    act(() => {
      jest.advanceTimersByTime(6000)
    })
    // Since no token is present, no refresh action should be dispatched.
    expect(store.dispatch).not.toHaveBeenCalled()
  })

  test('dispatches logout if token is expired', async () => {
    // Simulate an expired token by making jwtDecode return an exp in the past.
    jwtDecode.mockImplementationOnce(() => ({ exp: Math.floor((Date.now() - 1000) / 1000) }))

    render(
      <Provider store={store}>
        <SessionManager />
      </Provider>
    )

    // Wait for logout to be dispatched.
    await waitFor(() => {
      expect(store.dispatch).toHaveBeenCalledWith(logout())
    })
  })
})
