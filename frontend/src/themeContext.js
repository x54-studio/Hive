// src/ThemeContext.js
import React, { createContext, useState, useEffect } from 'react'

const ThemeContext = createContext()

const ThemeProvider = ({ children }) => {
  // Get initial theme from localStorage or default to "light"
  const storedTheme = localStorage.getItem('theme') || 'light'
  const [theme, setTheme] = useState(storedTheme)

  useEffect(() => {
    const root = document.documentElement // the <html> element
    // Remove any previous theme classes
    root.classList.remove('light', 'dark')
    // Add the current theme class
    root.classList.add(theme)
    // Save theme to localStorage for persistence
    localStorage.setItem('theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'))
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export { ThemeContext, ThemeProvider }
