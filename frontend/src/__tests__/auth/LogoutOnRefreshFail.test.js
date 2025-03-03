// src/__tests__/auth/LogoutOnRefreshFail.test.js
import axiosInstance, { setStore } from '../../api/axiosInstance'
import MockAdapter from 'axios-mock-adapter'
import { createAppStore } from '../../redux/store'

describe('Automatic logout on token refresh failure', () => {
  let mock, store

  beforeEach(() => {
    // Create a fresh store instance with initial user data for the test.
    store = createAppStore({
      auth: { user: { username: 'testUser', email: 'test@example.com' }, loading: false, error: null },
    })
    // Inject the test store into the axios instance.
    setStore(store)
    mock = new MockAdapter(axiosInstance)
  })

  afterEach(() => {
    mock.restore()
  })

  test('clears user data when token refresh fails', async () => {
    // Simulate a protected endpoint call returning 401 (Unauthorized)
    mock.onGet('/protected').replyOnce(401)
    // Simulate the refresh endpoint returning an error
    mock.onPost('/refresh').replyOnce(400, { error: 'Refresh failed' })

    try {
      await axiosInstance.get('/protected')
    } catch (error) {
      // Expected failure.
    }

    // Verify that the store's auth state has cleared the user data.
    const state = store.getState().auth
    expect(state.user).toBeNull()
  })
})
