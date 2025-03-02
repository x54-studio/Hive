// src/__tests__/Register.test.js
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import { MemoryRouter } from 'react-router-dom'
import authReducer from '../redux/slices/authSlice'
import Register from '../pages/Register'
import { toast } from 'react-toastify'

// Instead of mocking axios directly, we mock our custom axiosInstance.
// Note: Adjust the relative path from __tests__ to api accordingly.
jest.mock('../api/axiosInstance', () => ({
  post: jest.fn(),
}))
import axiosInstance from '../api/axiosInstance'

// Mock react-toastify to prevent loading CSS and to spy on toast calls.
jest.mock('react-toastify', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  },
  ToastContainer: () => <div data-testid="toast-container" />,
}))

// Mock react-router-dom entirely within the module factory.
jest.mock('react-router-dom', () => {
  const actual = jest.requireActual('react-router-dom')
  const navigateMock = jest.fn()
  return {
    ...actual,
    useNavigate: () => navigateMock,
    __navigateMock: navigateMock,
  }
})
import { __navigateMock } from 'react-router-dom'

describe('Register Component', () => {
  let store

  beforeEach(() => {
    __navigateMock.mockReset()
    store = configureStore({
      reducer: { auth: authReducer },
    })
  })

  const renderWithProviders = (ui) =>
    render(
      <Provider store={store}>
        <MemoryRouter>{ui}</MemoryRouter>
      </Provider>
    )

  test('renders registration form and submits valid data', async () => {
    axiosInstance.post.mockResolvedValueOnce({
      data: { message: 'User registered successfully!', user_id: '12345' },
    })

    renderWithProviders(<Register />)

    const usernameInput = screen.getByPlaceholderText(/username/i)
    const emailInput = screen.getByPlaceholderText(/email/i)
    const passwordInput = screen.getByPlaceholderText(/^password$/i)
    const confirmPasswordInput = screen.getByPlaceholderText('Confirm Password')
    const registerButton = screen.getByRole('button', { name: /register/i })

    fireEvent.change(usernameInput, { target: { value: 'newUser' } })
    fireEvent.change(emailInput, { target: { value: 'newuser@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } })
    fireEvent.click(registerButton)

    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith(
        'User registered successfully! Please log in.'
      )
      expect(__navigateMock).toHaveBeenCalledWith('/login')
    })
  })

  test('displays error message when registration fails', async () => {
    axiosInstance.post.mockRejectedValueOnce({
      response: { data: { error: 'A user with this username or email already exists.' } },
    })

    renderWithProviders(<Register />)

    const usernameInput = screen.getByPlaceholderText(/username/i)
    const emailInput = screen.getByPlaceholderText(/email/i)
    const passwordInput = screen.getByPlaceholderText(/^password$/i)
    const confirmPasswordInput = screen.getByPlaceholderText('Confirm Password')
    const registerButton = screen.getByRole('button', { name: /register/i })

    fireEvent.change(usernameInput, { target: { value: 'existingUser' } })
    fireEvent.change(emailInput, { target: { value: 'existing@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.change(confirmPasswordInput, { target: { value: 'password123' } })
    fireEvent.click(registerButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith(
        'A user with this username or email already exists.'
      )
    })
  })
})
