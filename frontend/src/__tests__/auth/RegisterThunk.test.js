// src/__tests__/auth/RegisterThunk.test.js
import { register } from '../../redux/slices/authSlice'
import axiosInstance from '../../api/axiosInstance'

// Mock the axiosInstance so that our register thunk uses our mocked functions
jest.mock('../../api/axiosInstance', () => ({
  post: jest.fn(),
  get: jest.fn(),
}))

describe('register thunk', () => {
  test('fulfills with user data on successful registration', async () => {
    // Simulate a successful registration response from the backend
    axiosInstance.post.mockResolvedValueOnce({
      data: { message: 'User registered successfully!', user_id: '12345' },
    })
    // For registration, no GET request is needed; the thunk only calls post.
    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = register({
      username: 'newUser',
      email: 'newuser@example.com',
      password: 'password123',
      confirmPassword: 'password123',
    })
    const result = await action(dispatch, getState, undefined)
    expect(result.payload).toEqual({
      message: 'User registered successfully!',
      user_id: '12345',
    })
  })

  test('rejects with error message on registration failure', async () => {
    // Simulate an error response from the backend for a duplicate registration
    axiosInstance.post.mockRejectedValueOnce({
      response: { data: { error: 'A user with this username or email already exists.' } },
    })
    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = register({
      username: 'existingUser',
      email: 'existing@example.com',
      password: 'password123',
      confirmPassword: 'password123',
    })
    const result = await action(dispatch, getState, undefined)
    expect(result.payload.error).toContain(
      'A user with this username or email already exists.'
    )
  })
})
