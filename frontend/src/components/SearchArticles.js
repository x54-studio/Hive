// src/components/SearchArticles.js
import React, { useState, useEffect, useRef } from 'react'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import ArticleCard from './ArticleCard'

const SearchArticles = () => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const abortControllerRef = useRef(null)

  const performSearch = async (searchQuery) => {
    // Cancel previous request if exists
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new AbortController for this request
    abortControllerRef.current = new AbortController()

    setLoading(true)
    setError('')
    
    try {
      const response = await axiosInstance.get('/articles/search', {
        params: { query: searchQuery },
        signal: abortControllerRef.current.signal
      })
      
      const articlesData = Array.isArray(response.data) ? response.data : []
      setResults(articlesData)
      
      if (articlesData.length === 0 && searchQuery.trim()) {
        setError('No articles found matching your search.')
      }
    } catch (err) {
      // Don't show error if request was aborted
      if (err.name === 'AbortError' || err.code === 'ERR_CANCELED') {
        return
      }
      
      const errorMessage = err.response?.data?.error || 'Failed to search articles'
      setError(errorMessage)
      toast.error(errorMessage, { autoClose: 5000 })
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  // Debounce effect: delays API call by 100ms after user stops typing
  useEffect(() => {
    if (!query.trim()) {
      setResults([])
      setError('')
      setLoading(false)
      // Cancel any pending request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      return
    }

    const timer = setTimeout(() => {
      performSearch(query.trim())
    }, 100)

    return () => {
      clearTimeout(timer)
      // Cancel request if component unmounts or query changes before timeout
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [query])


  return (
    <div className="w-full">
      <div className="mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search articles by title..."
          className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-lg"
          autoFocus
        />
        {loading && (
          <div className="mt-2 text-gray-600 text-sm">Searching...</div>
        )}
      </div>

      {error && !loading && (
        <div className="text-center py-8 text-gray-600">
          {error}
        </div>
      )}

      {!loading && !error && query.trim() && results.length === 0 && (
        <div className="text-center py-8 text-gray-600">
          No articles found matching "{query}"
        </div>
      )}

      {!loading && results.length > 0 && (
        <div>
          <div className="mb-4 text-sm text-gray-600">
            Found {results.length} {results.length === 1 ? 'article' : 'articles'}
          </div>
          <div>
            {results.map((article) => (
              <ArticleCard key={article.article_id || article._id} article={article} />
            ))}
          </div>
        </div>
      )}

      {!query.trim() && (
        <div className="text-center py-8 text-gray-500">
          Enter a search query to find articles
        </div>
      )}
    </div>
  )
}

export default SearchArticles

