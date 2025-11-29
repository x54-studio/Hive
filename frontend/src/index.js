// src/index.js
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { Provider } from 'react-redux'
import { store } from './redux/store'
import './styles/index.css'
import { setStore } from './api/axiosInstance'
import ErrorBoundary from './components/ErrorBoundary'

// Inject the store into the axios instance.
setStore(store)

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <ErrorBoundary>
    <Provider store={store}>
      <App />
    </Provider>
  </ErrorBoundary>
)
