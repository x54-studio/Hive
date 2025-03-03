// src/api/axiosInstance.js
import axios from 'axios'
import { API_BASE_URL } from '../config'
import { logout } from '../redux/slices/authSlice'

// Initially, appStore is undefined.
let appStore

// A flag to disable further refresh attempts after a failure.
let isRefreshingFailed = false

// Setter to inject the store (use in production and tests)
export const setStore = (store) => {
  appStore = store
  // Reset the flag on a fresh store/login.
  isRefreshingFailed = false
}

const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  withCredentials: true,
})

axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // If the failing request is for the refresh endpoint or if refresh has already failed,
    // immediately reject without retrying.
    if (
      (originalRequest.url === '/refresh') ||
      isRefreshingFailed
    ) {
      return Promise.reject(error)
    }

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        // Attempt to refresh the token.
        await axiosInstance.post('/refresh', {}, { withCredentials: true })
        // If refresh succeeds, reset the flag and retry the original request.
        isRefreshingFailed = false
        return axiosInstance(originalRequest)
      } catch (refreshError) {
        // On refresh failure, set the flag and dispatch logout to clear user data.
        isRefreshingFailed = true
        if (appStore) {
          await appStore.dispatch(logout())
        }
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
