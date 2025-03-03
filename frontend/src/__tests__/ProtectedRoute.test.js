// src/__tests__/ProtectedRoute.test.js
import React from 'react'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import authReducer from '../redux/slices/authSlice'
import ProtectedRoute from '../components/ProtectedRoute'
import Profile from '../pages/Profile'

describe('ProtectedRoute', () => {
  const renderWithProviders = (store, initialEntries) => {
    return render(
      <Provider store={store}>
        <MemoryRouter initialEntries={initialEntries}>
          <Routes>
            <Route element={<ProtectedRoute />}>
              <Route path="/profile" element={<Profile />} />
            </Route>
            <Route path="/login" element={<div data-testid="login-page">Login Page</div>} />
          </Routes>
        </MemoryRouter>
      </Provider>
    )
  }

  test('redirects to login when user is not authenticated', () => {
    const store = configureStore({
      reducer: { auth: authReducer },
      preloadedState: { auth: { user: null, loading: false, error: null } },
    })

    renderWithProviders(store, ['/profile'])
    // Use test id to ensure a unique match.
    expect(screen.getByTestId('login-page')).toBeInTheDocument()
  })

  test('renders protected component when user is authenticated', () => {
    const store = configureStore({
      reducer: { auth: authReducer },
      preloadedState: {
        auth: { user: { username: 'testUser', email: 'test@example.com' }, loading: false, error: null },
      },
    })

    renderWithProviders(store, ['/profile'])
    // Assume Profile component renders "Profile Page"
    expect(screen.getByText(/profile page/i)).toBeInTheDocument()
  })
})
