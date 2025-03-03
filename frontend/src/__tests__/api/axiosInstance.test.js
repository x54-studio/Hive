// src/__tests__/api/axiosInstance.test.js
import axiosInstance from '../../api/axiosInstance'
import MockAdapter from 'axios-mock-adapter'

describe('axiosInstance interceptor for token refresh', () => {
  let mock

  beforeEach(() => {
    mock = new MockAdapter(axiosInstance)
  })

  afterEach(() => {
    mock.restore()
  })

  test('retries the original request after a successful refresh', async () => {
    // Simulate the original request to /protected returning 401 (Unauthorized)
    mock.onGet('/protected').replyOnce(401)
    // Simulate a successful refresh endpoint call
    mock.onPost('/refresh').replyOnce(200)
    // After refreshing, simulate a successful response from the retried original request
    mock.onGet('/protected').replyOnce(200, { data: 'success' })

    const response = await axiosInstance.get('/protected')
    expect(response.data).toEqual({ data: 'success' })
  })

  test('rejects the promise if refresh fails', async () => {
    // Simulate the original request to /protected returning 401 (Unauthorized)
    mock.onGet('/protected').replyOnce(401)
    // Simulate a failed refresh attempt
    mock.onPost('/refresh').replyOnce(400, { error: 'Refresh failed' })

    try {
      await axiosInstance.get('/protected')
      throw new Error('Expected request to fail')
    } catch (error) {
      expect(error.response.data).toEqual({ error: 'Refresh failed' })
    }
  })
})
