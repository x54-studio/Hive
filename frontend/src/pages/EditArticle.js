// src/pages/EditArticle.js
import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import ArticleForm from '../components/ArticleForm'

const EditArticle = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchArticle = async () => {
      setLoading(true)
      setError('')
      try {
        const response = await axiosInstance.get(`/articles/${id}`)
        setArticle(response.data)
        
        // Check authorization: admin/moderator OR author
        const role = user?.claims?.role || user?.role
        const username = user?.username || user?.claims?.username
        const canEdit = role === 'admin' || role === 'moderator' || username === response.data.author
        
        if (!canEdit) {
          toast.error('You do not have permission to edit this article', { autoClose: 3000 })
          navigate(`/articles/${id}`)
        }
      } catch (err) {
        if (err.response?.status === 404) {
          setError('Article not found')
        } else {
          const errorMessage = err.response?.data?.error || 'Failed to load article'
          setError(errorMessage)
          toast.error(errorMessage, { autoClose: 5000 })
        }
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchArticle()
    }
  }, [id, user, navigate])

  const handleSubmit = async (title, content) => {
    setIsSubmitting(true)
    try {
      await axiosInstance.put(`/articles/${id}`, { title, content })
      toast.success('Article updated successfully', { autoClose: 2000 })
      navigate(`/articles/${id}`)
    } catch (err) {
      if (err.response?.status === 404) {
        toast.error('Article not found', { autoClose: 5000 })
        navigate('/articles')
      } else if (err.response?.status === 400) {
        const errorMessage = err.response?.data?.error || 'Invalid article data'
        toast.error(errorMessage, { autoClose: 5000 })
      } else {
        const errorMessage = err.response?.data?.error || 'Failed to update article'
        toast.error(errorMessage, { autoClose: 5000 })
      }
      throw err
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancel = () => {
    navigate(`/articles/${id}`)
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading article...</div>
      </div>
    )
  }

  if (error && !article) {
    return (
      <div className="p-8 max-w-4xl mx-auto">
        <div className="text-center py-12">
          <div className="text-red-600 text-lg mb-4">{error}</div>
          <button
            onClick={() => navigate('/articles')}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Back to Articles
          </button>
        </div>
      </div>
    )
  }

  if (!article) {
    return null
  }

  // Double-check authorization before rendering form
  const role = user?.claims?.role || user?.role
  const username = user?.username || user?.claims?.username
  const canEdit = role === 'admin' || role === 'moderator' || username === article.author

  if (!canEdit) {
    return null
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Edit Article</h2>
      <ArticleForm
        initialData={{ title: article.title, content: article.content }}
        onSubmit={handleSubmit}
        submitLabel="Update Article"
        isLoading={isSubmitting}
        onCancel={handleCancel}
      />
    </div>
  )
}

export default EditArticle

