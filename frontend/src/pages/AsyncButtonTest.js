// src/pages/AsyncButtonTest.js
import React from 'react'
import AsyncButton from '../components/AsyncButton'

const AsyncButtonTest = () => {
  const asyncOperation = () =>
    new Promise((resolve) => {
      setTimeout(() => {
        resolve()
      }, 2000) // simulate a 2-second async operation
    })

  return (
    <div>
      <h2>Async Button Test</h2>
      <AsyncButton
        data-cy="async-button"
        initialLabel="Submit"
        loadingLabel="Processing..."
        onClick={asyncOperation}
      />
    </div>
  )
}

export default AsyncButtonTest
