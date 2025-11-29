// src/api/axiosInstance.js
import axios from 'axios'
import { API_BASE_URL } from '../config'
import { logout, refresh } from '../redux/slices/authSlice'

let appStore

export const setStore = (store) => {
  appStore = store
}

const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  withCredentials: true,
})

// Request interceptor: cookies are automatically sent with requests
// No need to manually add Authorization header since backend uses cookies
axiosInstance.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => Promise.reject(error)
)

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Don't retry refresh endpoint failures
    if (originalRequest.url.includes('/refresh')) {
      return Promise.reject(error)
    }

    // Handle 401 errors by attempting token refresh
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      // Ensure appStore is available before attempting refresh
      if (!appStore) {
        return Promise.reject(error)
      }

      try {
        const refreshResult = await appStore.dispatch(refresh())
        // If refresh failed, logout
        if (refresh.fulfilled.match(refreshResult)) {
          // Retry the original request with new token
          return axiosInstance(originalRequest)
        } else {
          // Refresh failed, logout user
          await appStore.dispatch(logout())
          return Promise.reject(error)
        }
      } catch (refreshError) {
        // Refresh threw an error, logout user
        await appStore.dispatch(logout())
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
