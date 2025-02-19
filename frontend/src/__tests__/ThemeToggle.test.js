import React from 'react'
import { render, fireEvent } from '@testing-library/react'
import ThemeToggle from '../components/ThemeToggle'
import { ThemeContext } from '../ThemeContext'

test('ThemeToggle calls toggleTheme when clicked', () => {
  const toggleTheme = jest.fn()
  const { getByRole } = render(
    <ThemeContext.Provider value={{ theme: 'light', toggleTheme }}>
      <ThemeToggle />
    </ThemeContext.Provider>
  )
  const button = getByRole('button')
  fireEvent.click(button)
  expect(toggleTheme).toHaveBeenCalledTimes(1)
})
