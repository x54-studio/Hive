// src/api/axiosInstance.js
import axios from 'axios';
import { logoutAsync, setUser } from '../redux/authSlice';
import { store } from '../redux/store'; // Ensure your store is exported as a named export

// Create an axios instance with your base URL and credentials.
const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  withCredentials: true,
});

// Response interceptor for handling 401 errors and token refresh.
axiosInstance.interceptors.response.use(
  (response) => {
    // If the response is successful, simply return it.
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    // Check if error status is 401 (Unauthorized)
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      // Prevent infinite loop: do not retry refresh endpoint calls
      !originalRequest.url.includes('/refresh')
    ) {
      originalRequest._retry = true;
      console.info("401 detected. Attempting to refresh tokens...");

      try {
        // Call your refresh endpoint using POST.
        const refreshResponse = await axiosInstance.post('/refresh', {}, { withCredentials: true });
        console.info("Refresh successful:", refreshResponse.data);

        // After successful refresh, fetch the updated user details.
        const protectedResponse = await axiosInstance.get('/protected', { withCredentials: true });
        console.info("Fetched updated user data:", protectedResponse.data);

        // Update the Redux state with the new user details.
        store.dispatch(setUser(protectedResponse.data));

        // Retry the original request with new credentials.
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        // If refresh fails, dispatch logout and redirect to login or home page.
        await store.dispatch(logoutAsync());
        window.location.href = '/';
        return Promise.reject(refreshError);
      }
    }
    // If the error is not 401 or refresh already attempted, reject the promise.
    return Promise.reject(error);
  }
);

export default axiosInstance;
