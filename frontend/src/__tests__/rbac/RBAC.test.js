// src/__tests__/rbac/RBAC.test.js
import React from 'react'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { createAppStore } from '../../redux/store'
import RBACDemo from '../../components/RBACDemo'

describe('RBAC Demo Component', () => {
  // Helper to render the component with a specific preloaded state.
  const renderWithStore = (preloadedState) => {
    const store = createAppStore(preloadedState)
    return render(
      <Provider store={store}>
        <RBACDemo />
      </Provider>
    )
  }

  test('displays login prompt when no user is logged in', () => {
    renderWithStore({ auth: { user: null, loading: false, error: null } })
    expect(screen.getByText(/please log in/i)).toBeInTheDocument()
  })

  test('displays admin dashboard for admin role', () => {
    renderWithStore({
      auth: { user: { role: 'admin', username: 'adminUser' }, loading: false, error: null },
    })
    expect(screen.getByText(/admin dashboard/i)).toBeInTheDocument()
  })

  test('displays moderator panel for moderator role', () => {
    renderWithStore({
      auth: { user: { role: 'moderator', username: 'moderatorUser' }, loading: false, error: null },
    })
    expect(screen.getByText(/moderator panel/i)).toBeInTheDocument()
  })

  test('displays user profile for regular user role', () => {
    renderWithStore({
      auth: { user: { role: 'regular', username: 'regularUser' }, loading: false, error: null },
    })
    expect(screen.getByText(/user profile/i)).toBeInTheDocument()
  })

  test('displays unknown role for unrecognized role', () => {
    renderWithStore({
      auth: { user: { role: 'superuser', username: 'mysteryUser' }, loading: false, error: null },
    })
    expect(screen.getByText(/unknown role/i)).toBeInTheDocument()
  })
})
