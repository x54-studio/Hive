import '@testing-library/jest-dom'
import React from 'react'
import { render, waitFor } from '@testing-library/react'
import { AuthProvider, AuthContext } from '../AuthContext'

// Dummy component to consume AuthContext
const DummyComponent = () => {
  const { user } = React.useContext(AuthContext)
  return <div>{user ? user.username : 'No user'}</div>
}

test('AuthContext fetches user profile on mount', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ username: 'testuser', role: 'admin' }),
    })
  )

  const { getByText } = render(
    <AuthProvider>
      <DummyComponent />
    </AuthProvider>
  )

  await waitFor(() => expect(getByText('testuser')).toBeInTheDocument())

  global.fetch.mockRestore()
})
