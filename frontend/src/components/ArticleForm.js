// src/components/ArticleForm.js
import React, { useState, useEffect } from 'react'
import AsyncButton from './AsyncButton'

const ArticleForm = ({ initialData, onSubmit, submitLabel, isLoading, onCancel }) => {
  const [title, setTitle] = useState(initialData?.title || '')
  const [content, setContent] = useState(initialData?.content || '')
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || '')
      setContent(initialData.content || '')
    }
  }, [initialData])

  const validate = () => {
    const newErrors = {}
    
    if (!title.trim()) {
      newErrors.title = 'Title is required'
    } else if (title.trim().length < 3) {
      newErrors.title = 'Title must be at least 3 characters'
    } else if (title.length > 200) {
      newErrors.title = 'Title must be less than 200 characters'
    }
    
    if (!content.trim()) {
      newErrors.content = 'Content is required'
    } else if (content.trim().length < 10) {
      newErrors.content = 'Content must be at least 10 characters'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!validate()) {
      return
    }
    
    try {
      await onSubmit(title.trim(), content.trim())
    } catch (error) {
      // Error handling is done by parent component
    }
  }

  const handleButtonClick = async (e) => {
    e.preventDefault()
    await handleSubmit(e)
  }

  return (
    <form onSubmit={handleSubmit} className="mt-4 p-4 border rounded max-w-3xl">
      <div className="mb-4">
        <label htmlFor="title" className="block mb-1 font-medium">
          Title
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value)
            if (errors.title) {
              setErrors({ ...errors, title: '' })
            }
          }}
          className={`border p-2 w-full ${errors.title ? 'border-red-500' : ''}`}
          disabled={isLoading}
          maxLength={200}
        />
        {errors.title && (
          <div className="text-red-600 text-sm mt-1">{errors.title}</div>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="content" className="block mb-1 font-medium">
          Content
        </label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => {
            setContent(e.target.value)
            if (errors.content) {
              setErrors({ ...errors, content: '' })
            }
          }}
          rows={12}
          className={`border p-2 w-full ${errors.content ? 'border-red-500' : ''}`}
          disabled={isLoading}
        />
        {errors.content && (
          <div className="text-red-600 text-sm mt-1">{errors.content}</div>
        )}
      </div>

      <div className="flex space-x-2 mt-4">
        <AsyncButton
          type="button"
          initialLabel={submitLabel || 'Submit'}
          loadingLabel="Submitting..."
          onClick={handleButtonClick}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        />
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            disabled={isLoading}
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}

export default ArticleForm

