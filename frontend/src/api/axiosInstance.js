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

// Add a request interceptor to include auth token if available.
axiosInstance.interceptors.request.use(
  (config) => {
    // Example: retrieve token from localStorage or state.
    const token = localStorage.getItem('token') // adjust as needed
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (originalRequest.url.includes('/refresh')) {
      return Promise.reject(error)
    }

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        await appStore.dispatch(refresh())
        return axiosInstance(originalRequest)
      } catch (refreshError) {
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
