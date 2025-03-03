// src/__tests__/auth/LogoutThunk.test.js
import { logout } from '../../redux/slices/authSlice'
import axiosInstance from '../../api/axiosInstance'

// Mock the axiosInstance to control the API responses
jest.mock('../../api/axiosInstance', () => ({
  post: jest.fn(),
}))

describe('logout thunk', () => {
  test('fulfills successfully when logout API returns success', async () => {
    // Simulate a successful logout response from the backend
    axiosInstance.post.mockResolvedValueOnce({ data: {} })
    
    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = logout()
    const result = await action(dispatch, getState, undefined)
    
    // On successful logout, the thunk should resolve without a payload
    expect(result.payload).toBeUndefined()
  })

  test('rejects with error message when logout fails', async () => {
    // Simulate an error response from the backend for logout
    axiosInstance.post.mockRejectedValueOnce({
      response: { data: { error: 'Logout failed' } },
    })
    
    const dispatch = jest.fn()
    const getState = jest.fn(() => ({}))
    const action = logout()
    const result = await action(dispatch, getState, undefined)
    
    // The thunk should reject with the error message from the response
    expect(result.payload).toEqual({ error: 'Logout failed' })
  })
})
