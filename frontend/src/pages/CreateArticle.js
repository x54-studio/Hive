// src/pages/CreateArticle.js
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import ArticleForm from '../components/ArticleForm'

const CreateArticle = () => {
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)
  const [isLoading, setIsLoading] = useState(false)

  // RBAC check: Only admin/moderator can create articles
  useEffect(() => {
    const role = user?.claims?.role || user?.role
    if (role !== 'admin' && role !== 'moderator') {
      toast.error('You do not have permission to create articles', { autoClose: 3000 })
      navigate('/articles')
    }
  }, [user, navigate])

  const handleSubmit = async (title, content) => {
    setIsLoading(true)
    try {
      const response = await axiosInstance.post('/articles', { title, content })
      
      if (response.data.article_id) {
        toast.success('Article created successfully', { autoClose: 2000 })
        // Redirect to the new article detail page
        navigate(`/articles/${response.data.article_id}`)
      } else {
        toast.success('Article created successfully', { autoClose: 2000 })
        navigate('/articles')
      }
    } catch (err) {
      if (err.response?.status === 403) {
        toast.error('You do not have permission to create articles', { autoClose: 5000 })
        navigate('/articles')
      } else if (err.response?.status === 400) {
        const errorMessage = err.response?.data?.error || 'Invalid article data'
        toast.error(errorMessage, { autoClose: 5000 })
      } else {
        const errorMessage = err.response?.data?.error || 'Failed to create article'
        toast.error(errorMessage, { autoClose: 5000 })
      }
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancel = () => {
    navigate('/articles')
  }

  const role = user?.claims?.role || user?.role
  if (role !== 'admin' && role !== 'moderator') {
    return null
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Create Article</h2>
      <ArticleForm
        onSubmit={handleSubmit}
        submitLabel="Create Article"
        isLoading={isLoading}
        onCancel={handleCancel}
      />
    </div>
  )
}

export default CreateArticle

