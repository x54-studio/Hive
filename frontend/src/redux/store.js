// src/redux/store.js
import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'

export function createAppStore(preloadedState) {
  return configureStore({
    reducer: {
      auth: authReducer,
    },
    preloadedState,
  })
}

// Export a default singleton store for production
export const store = createAppStore()
