// src/pages/Search.js
import React from 'react'
import SearchArticles from '../components/SearchArticles'

const Search = () => {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Search Articles</h2>
      <SearchArticles />
    </div>
  )
}

export default Search

