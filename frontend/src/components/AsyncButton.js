// src/components/AsyncButton.js
import React, { useState } from 'react'

const AsyncButton = ({ onClick, initialLabel, loadingLabel, ...props }) => {
  const [isLoading, setIsLoading] = useState(false)

  const handleClick = async (e) => {
    if (isLoading) return
    setIsLoading(true)
    try {
      await onClick(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button onClick={handleClick} disabled={isLoading} {...props}>
      {isLoading ? (loadingLabel || 'Loading...') : initialLabel}
    </button>
  )
}

export default AsyncButton
