// src/components/ArticleCard.js
import React from 'react'
import { Link } from 'react-router-dom'

const ArticleCard = ({ article }) => {
  const truncateContent = (content, maxLength = 150) => {
    if (!content) return ''
    if (content.length <= maxLength) return content
    return content.substring(0, maxLength) + '...'
  }

  const formatDate = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    } catch (error) {
      return dateString
    }
  }

  return (
    <Link
      to={`/articles/${article.article_id}`}
      className="block p-6 bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-lg transition-shadow duration-200 mb-4"
    >
      <h3 className="text-xl font-bold text-gray-900 mb-2">{article.title}</h3>
      <p className="text-gray-600 mb-4 line-clamp-3">{truncateContent(article.content)}</p>
      <div className="flex justify-between items-center text-sm text-gray-500">
        <span className="font-medium">By {article.author}</span>
        <span>{formatDate(article.created_at)}</span>
      </div>
    </Link>
  )
}

export default ArticleCard

