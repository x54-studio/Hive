// src/redux/slices/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import axiosInstance from '../../api/axiosInstance'

export const login = createAsyncThunk(
  'auth/login',
  async ({ username_or_email, password }, { rejectWithValue }) => {
    try {
      await axiosInstance.post(
        '/login',
        { username_or_email, password },
        { withCredentials: true }
      )
      const userResp = await axiosInstance.get('/protected', { withCredentials: true })
      return userResp.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Login failed')
    }
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async ({ username, email, password, confirmPassword }, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.post(
        '/register',
        { username, email, password, confirmPassword },
        { withCredentials: true }
      )
      return response.data
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Registration failed')
    }
  }
)

export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await axiosInstance.post('/logout', {}, { withCredentials: true })
      return
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Logout failed')
    }
  }
)

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, loading: false, error: null },
  reducers: {
    clearError(state) {
      state.error = null
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false
        state.user = action.payload
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(register.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(register.fulfilled, (state) => {
        state.loading = false
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(logout.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(logout.fulfilled, (state) => {
        state.loading = false
        state.user = null
      })
      .addCase(logout.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
  }
})

export const { clearError } = authSlice.actions
export default authSlice.reducer
