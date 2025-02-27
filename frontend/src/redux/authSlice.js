// src/redux/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Initial state for authentication.
const initialState = {
  user: null,
  loading: false,
  error: null,
};

// Thunk for login.
export const login = createAsyncThunk(
  'auth/login',
  async (credentials, { rejectWithValue, dispatch }) => {
    try {
      // Send login request; backend sets cookies.
      await axios.post('http://localhost:5000/api/login', credentials, { withCredentials: true });
      // After a successful login, fetch user details.
      const response = await axios.get('http://localhost:5000/api/protected', { withCredentials: true });
      dispatch(setUser(response.data));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Thunk for logout.
export const logoutAsync = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await axios.post('http://localhost:5000/api/logout', {}, { withCredentials: true });
      return;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Thunk for refreshing tokens using POST.
export const refreshTokens = createAsyncThunk(
  'auth/refreshTokens',
  async (_, { rejectWithValue, dispatch }) => {
    try {
      // Use POST to call the refresh endpoint.
      const response = await axios.post('http://localhost:5000/api/refresh', {}, { withCredentials: true });
      const protectedResponse = await axios.get('http://localhost:5000/api/protected', { withCredentials: true });
      dispatch(setUser(protectedResponse.data));
      return protectedResponse.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(logoutAsync.fulfilled, (state) => {
        state.user = null;
        state.error = null;
      })
      .addCase(refreshTokens.fulfilled, (state, action) => {
        // Update user state with the new token data.
        state.user = action.payload;
      });
  },
});

export const { setUser } = authSlice.actions;
export default authSlice.reducer;
