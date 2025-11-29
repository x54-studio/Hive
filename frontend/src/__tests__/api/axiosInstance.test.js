// src/__tests__/api/axiosInstance.test.js
import axiosInstance, { setStore } from '../../api/axiosInstance'
import MockAdapter from 'axios-mock-adapter'

// Create mock action results
const mockRefreshFulfilled = { type: 'auth/refresh/fulfilled', payload: {} }
const mockRefreshRejected = { type: 'auth/refresh/rejected', payload: { error: 'Refresh failed' } }

// Mock the auth actions so they return predictable action objects.
jest.mock('../../redux/slices/authSlice', () => {
  const mockRefreshFn = jest.fn()
  mockRefreshFn.fulfilled = { match: (action) => action?.type === 'auth/refresh/fulfilled' }
  mockRefreshFn.rejected = { match: (action) => action?.type === 'auth/refresh/rejected' }
  mockRefreshFn.pending = { match: (action) => action?.type === 'auth/refresh/pending' }
  
  return {
    refresh: mockRefreshFn,
    logout: jest.fn(() => ({ type: 'auth/logout' }))
  }
})

// Import the mocked functions after jest.mock
import { refresh, logout } from '../../redux/slices/authSlice'

// Create a dummy store with a mocked dispatch method.
const dummyStore = {
  dispatch: jest.fn((action) => {
    if (typeof action === 'function') {
      return action()
    }
    return Promise.resolve(action)
  }),
}

describe('axiosInstance interceptor for token refresh', () => {
  let mock

  beforeEach(() => {
    // Set the dummy store so the interceptor uses it.
    setStore(dummyStore)
    dummyStore.dispatch.mockClear()
    refresh.mockClear()
    logout.mockClear()
    mock = new MockAdapter(axiosInstance)

    refresh.mockImplementation(() => () => Promise.resolve(mockRefreshFulfilled))
  })

  afterEach(() => {
    mock.restore()
  })

  test('retries the original request after a successful refresh', async () => {
    const protectedPattern = /\/(api\/)?protected$/
    const refreshPattern = /\/(api\/)?refresh$/
    let protectedCallCount = 0

    mock.onGet(protectedPattern).reply(() => {
      protectedCallCount += 1
      if (protectedCallCount === 1) {
        return [401, {}]
      }
      return [200, { data: 'success' }]
    })
    
    mock.onPost(refreshPattern).reply(200, { 
      message: 'Token refreshed successfully',
      username: 'testuser',
      claims: { exp: Math.floor((Date.now() + 900000) / 1000) }
    })

    const refreshSuccessResult = {
      type: 'auth/refresh/fulfilled',
      payload: {
        message: 'Token refreshed successfully',
        username: 'testuser',
        claims: { exp: Math.floor((Date.now() + 900000) / 1000) }
      }
    }
    refresh.mockImplementation(() => () => Promise.resolve(refreshSuccessResult))

    const response = await axiosInstance.get('/protected')
    expect(response.data).toEqual({ data: 'success' })

    // Verify that refresh was called
    expect(refresh).toHaveBeenCalled()
    // Verify that /protected was called twice (original + retry)
    expect(protectedCallCount).toBe(2)
  })

  test('rejects the promise if refresh fails and dispatches logout', async () => {
    // Simulate GET /protected returns 401.
    mock.onGet('/protected').replyOnce(401)
    refresh.mockImplementationOnce(() => () => Promise.resolve(mockRefreshRejected))

    let caughtError
    try {
      await axiosInstance.get('/protected')
      throw new Error('Expected request to fail')
    } catch (error) {
      caughtError = error
    }
    // Assert that the error object is what we expect.
    expect(caughtError).toBeDefined()
    // Error could be from the original 401 or from the refresh failure
    if (caughtError.response) {
      expect(caughtError.response.status).toBe(401)
    }

    // Verify that refresh was called
    expect(refresh).toHaveBeenCalled()

    // Verify that logout was called
    expect(logout).toHaveBeenCalled()
  })
})
