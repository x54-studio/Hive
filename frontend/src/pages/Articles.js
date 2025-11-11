// src/pages/Articles.js
import React from 'react'
import ArticleList from '../components/ArticleList'

const Articles = () => {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Articles</h2>
      <ArticleList />
    </div>
  )
}

export default Articles

