// src/components/ArticleList.js
import React, { useState, useEffect } from 'react'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import ArticleCard from './ArticleCard'

const ArticleList = () => {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const limit = 10

  const fetchArticles = async (page) => {
    setLoading(true)
    setError('')
    try {
      const response = await axiosInstance.get('/articles', {
        params: { page, limit }
      })
      
      const articlesData = Array.isArray(response.data) ? response.data : []
      setArticles(articlesData)
      setHasMore(articlesData.length === limit)
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'Failed to load articles'
      setError(errorMessage)
      toast.error(errorMessage, { autoClose: 5000 })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchArticles(currentPage)
  }, [currentPage])

  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  const handleNext = () => {
    if (hasMore) {
      setCurrentPage(currentPage + 1)
    }
  }

  if (loading && articles.length === 0) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading articles...</div>
      </div>
    )
  }

  if (error && articles.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={() => fetchArticles(currentPage)}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (articles.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-600 text-lg">No articles found.</div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        {articles.map((article) => (
          <ArticleCard key={article.article_id} article={article} />
        ))}
      </div>

      {loading && articles.length > 0 && (
        <div className="text-center text-gray-600 py-4">Loading...</div>
      )}

      <div className="flex justify-between items-center mt-6">
        <button
          onClick={handlePrevious}
          disabled={currentPage === 1 || loading}
          className={`px-4 py-2 rounded ${
            currentPage === 1 || loading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          Previous
        </button>

        <span className="text-gray-600">Page {currentPage}</span>

        <button
          onClick={handleNext}
          disabled={!hasMore || loading}
          className={`px-4 py-2 rounded ${
            !hasMore || loading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default ArticleList

