// src/__tests__/ErrorBoundary.test.js
import React from 'react'
import { render, screen } from '@testing-library/react'
import ErrorBoundary from '../components/ErrorBoundary'

function ProblemChild() {
  throw new Error('Test error')
}

describe('ErrorBoundary Component', () => {
  // Suppress console.error for this test block to avoid expected error logs.
  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterAll(() => {
    console.error.mockRestore()
  })

  test('displays fallback UI when an error is thrown', () => {
    render(
      <ErrorBoundary>
        <ProblemChild />
      </ErrorBoundary>
    )
    
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
    expect(screen.getByText(/please try refreshing/i)).toBeInTheDocument()
  })
})
