// src/__tests__/PersistLogin.test.js
import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { Provider } from 'react-redux'
import { createAppStore } from '../redux/store'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import PersistLogin from '../components/PersistLogin'
import ProtectedRoute from '../components/ProtectedRoute'
import Profile from '../pages/Profile'
import axiosInstance from '../api/axiosInstance'
import MockAdapter from 'axios-mock-adapter'

describe('PersistLogin Component', () => {
  let store, mock

  beforeEach(() => {
    store = createAppStore({
      auth: { user: null, loading: false, error: null },
    })
    mock = new MockAdapter(axiosInstance)
  })

  afterEach(() => {
    mock.restore()
  })

  test('displays loading state while refreshing and then renders protected content on success', async () => {
    // Simulate a delayed successful response for GET /protected with a shorter delay.
    mock.onGet('/protected').reply(() =>
      new Promise((resolve) =>
        setTimeout(() => resolve([200, { username: 'persistUser', email: 'persist@example.com' }]), 100)
      )
    )

    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={['/profile']}>
          <Routes>
            <Route element={<PersistLogin />}>
              <Route element={<ProtectedRoute />}>
                <Route path="/profile" element={<Profile />} />
              </Route>
            </Route>
            <Route path="/login" element={<div>Login Page</div>} />
          </Routes>
        </MemoryRouter>
      </Provider>
    )

    // Immediately after render, the "Loading..." indicator should be present.
    expect(screen.getByText(/loading/i)).toBeInTheDocument()

    // Wait for the refreshUser thunk to complete and for the Profile component to be rendered.
    await waitFor(() => {
      expect(screen.getByText(/profile page/i)).toBeInTheDocument()
    }, { timeout: 500 })
  })

  test('redirects to login if refresh fails', async () => {
    // Simulate a delayed failure response for GET /protected with a shorter delay.
    mock.onGet('/protected').reply(() =>
      new Promise((resolve) =>
        setTimeout(() => resolve([400, { error: 'Refresh failed' }]), 100)
      )
    )

    render(
      <Provider store={store}>
        <MemoryRouter initialEntries={['/profile']}>
          <Routes>
            <Route element={<PersistLogin />}>
              <Route element={<ProtectedRoute />}>
                <Route path="/profile" element={<Profile />} />
              </Route>
            </Route>
            <Route path="/login" element={<div>Login Page</div>} />
          </Routes>
        </MemoryRouter>
      </Provider>
    )

    // Wait for redirection to the login page.
    await waitFor(() => {
      expect(screen.getByText(/login page/i)).toBeInTheDocument()
    }, { timeout: 500 })
  })
})
