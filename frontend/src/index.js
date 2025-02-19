// src/index.js
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ThemeProvider } from './ThemeContext' // if using a theme context
import './styles/index.css' // Ensure global styles are imported

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <ThemeProvider>
    <App />
  </ThemeProvider>
)
