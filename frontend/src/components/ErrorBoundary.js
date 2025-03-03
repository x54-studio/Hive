// src/components/ErrorBoundary.js
import React from 'react'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render shows the fallback UI.
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    // You can log the error to an error reporting service here.
    console.error('Uncaught error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      // Fallback UI when an error is caught.
      return (
        <div className="p-4 bg-red-100 text-red-800">
          <h1>Something went wrong.</h1>
          <p>Please try refreshing the page or contact support.</p>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
