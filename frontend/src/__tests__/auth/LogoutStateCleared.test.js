// src/__tests__/auth/LogoutStateCleared.test.js
import { configureStore } from '@reduxjs/toolkit'
import authReducer, { logout } from '../../redux/slices/authSlice'
import axiosInstance from '../../api/axiosInstance'

// Mock axiosInstance to control the API responses
jest.mock('../../api/axiosInstance', () => ({
  post: jest.fn(),
}))

describe('Logout clears user data even on error', () => {
  test('clears user data on logout error', async () => {
    // Set up initial state with user data
    const preloadedState = {
      user: { username: 'testUser', email: 'test@example.com' },
      loading: false,
      error: null,
    }
    
    // Create a store with the authReducer and preloaded state
    const store = configureStore({
      reducer: { auth: authReducer },
      preloadedState: { auth: preloadedState }
    })
    
    // Simulate an error response from the logout API call
    axiosInstance.post.mockRejectedValueOnce({
      response: { data: { error: 'Logout failed' } },
    })
    
    await store.dispatch(logout())
    
    // Verify that user data is cleared even if logout fails
    const state = store.getState().auth
    expect(state.user).toBeNull()
    expect(state.error).toEqual({ error: 'Logout failed' })
  })
})
