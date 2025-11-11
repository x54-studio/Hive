// src/pages/ArticleDetail.js
import React, { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import AsyncButton from '../components/AsyncButton'

const ArticleDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const user = useSelector((state) => state.auth.user)
  const [article, setArticle] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const fetchArticle = async () => {
      setLoading(true)
      setError('')
      try {
        const response = await axiosInstance.get(`/articles/${id}`)
        setArticle(response.data)
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
  }, [id])

  const formatDate = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch (error) {
      return dateString
    }
  }

  const canEditArticle = (article, user) => {
    if (!article || !user) return false
    const role = user?.claims?.role || user?.role
    const username = user?.username || user?.claims?.username
    return role === 'admin' || role === 'moderator' || username === article.author
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this article? This action cannot be undone.')) {
      return
    }

    setIsDeleting(true)
    try {
      await axiosInstance.delete(`/articles/${id}`)
      toast.success('Article deleted successfully', { autoClose: 2000 })
      navigate('/articles')
    } catch (err) {
      if (err.response?.status === 404) {
        toast.error('Article not found', { autoClose: 5000 })
        navigate('/articles')
      } else {
        const errorMessage = err.response?.data?.error || 'Failed to delete article'
        toast.error(errorMessage, { autoClose: 5000 })
      }
    } finally {
      setIsDeleting(false)
    }
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

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={() => navigate('/articles')}
          className="text-blue-600 hover:text-blue-800 hover:underline"
        >
          ← Back to Articles
        </button>
        
        {canEditArticle(article, user) && (
          <div className="flex space-x-2">
            <Link
              to={`/articles/${id}/edit`}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Edit
            </Link>
            <AsyncButton
              onClick={handleDelete}
              initialLabel="Delete"
              loadingLabel="Deleting..."
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            />
          </div>
        )}
      </div>

      <article>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{article.title}</h1>
        
        <div className="flex items-center gap-4 text-sm text-gray-600 mb-6 pb-4 border-b">
          <span className="font-medium">By {article.author}</span>
          <span>•</span>
          <span>Created: {formatDate(article.created_at)}</span>
          {article.updated_at && article.updated_at !== article.created_at && (
            <>
              <span>•</span>
              <span>Updated: {formatDate(article.updated_at)}</span>
            </>
          )}
        </div>

        <div className="prose max-w-none">
          <div className="text-gray-800 whitespace-pre-wrap leading-relaxed">
            {article.content}
          </div>
        </div>
      </article>
    </div>
  )
}

export default ArticleDetail

