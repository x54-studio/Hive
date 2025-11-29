// src/__tests__/auth/LoginThunk.test.js
import { login } from '../../redux/slices/authSlice'
import axiosInstance from '../../api/axiosInstance'

// Mock axiosInstance to control API responses
jest.mock('../../api/axiosInstance', () => ({
  post: jest.fn(),
  get: jest.fn(),
}))

describe('login thunk', () => {
  test('fulfills with user data on successful login', async () => {
    // Simulate a successful POST /login response with user data and claims
    const futureExp = Math.floor((Date.now() + 900000) / 1000)
    axiosInstance.post.mockResolvedValueOnce({ 
      data: { 
        message: 'Login successful',
        username: 'testUser',
        claims: { exp: futureExp }
      }
    })

    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = login({ username_or_email: 'testUser', password: 'password123' })
    const result = await action(dispatch, getState, undefined)

    expect(result.payload).toEqual({ 
      username: 'testUser', 
      claims: { exp: futureExp }
    })
  })

  test('rejects with error message on failed login', async () => {
    // Simulate an error response from the backend
    axiosInstance.post.mockRejectedValueOnce({
      response: { data: { error: 'Invalid credentials' } },
    })

    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = login({ username_or_email: 'wrongUser', password: 'wrongPass' })
    const result = await action(dispatch, getState, undefined)

    // The rejected payload should match the error message from the response
    expect(result.payload).toEqual({ error: 'Invalid credentials' })
  })
})
