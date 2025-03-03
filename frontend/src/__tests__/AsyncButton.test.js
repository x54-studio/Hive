// src/__tests__/AsyncButton.test.js
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import AsyncButton from '../components/AsyncButton'

describe('AsyncButton Component', () => {
  test('displays initial label and is enabled', () => {
    render(<AsyncButton initialLabel="Submit" onClick={jest.fn()} />)
    const button = screen.getByRole('button')
    expect(button).toHaveTextContent('Submit')
    expect(button).not.toBeDisabled()
  })

  test('displays loading label and disables while async operation is pending', async () => {
    let resolvePromise
    const asyncOperation = new Promise((resolve) => {
      resolvePromise = resolve
    })

    const onClick = jest.fn(() => asyncOperation)

    render(
      <AsyncButton
        initialLabel="Submit"
        loadingLabel="Processing..."
        onClick={onClick}
      />
    )

    const button = screen.getByRole('button')
    fireEvent.click(button)

    // Immediately after clicking, the button should be disabled and show loading label.
    expect(onClick).toHaveBeenCalledTimes(1)
    expect(button).toBeDisabled()
    expect(button).toHaveTextContent('Processing...')

    // Resolve the async operation
    resolvePromise()

    // Wait for the button to be re-enabled and display the initial label again.
    await waitFor(() => {
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent('Submit')
    })
  })

  test('prevents multiple clicks during async operation', async () => {
    let resolvePromise
    const asyncOperation = new Promise((resolve) => {
      resolvePromise = resolve
    })

    const onClick = jest.fn(() => asyncOperation)

    render(
      <AsyncButton
        initialLabel="Save"
        loadingLabel="Saving..."
        onClick={onClick}
      />
    )

    const button = screen.getByRole('button')
    fireEvent.click(button)
    fireEvent.click(button)
    fireEvent.click(button)

    // onClick should only have been called once.
    expect(onClick).toHaveBeenCalledTimes(1)

    // Resolve the promise
    resolvePromise()

    await waitFor(() => {
      expect(button).not.toBeDisabled()
    })
  })
})
