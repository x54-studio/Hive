import React, { useEffect, useState, useRef, useCallback } from 'react'
import axiosInstance from '../api/axiosInstance'
import { toast } from 'react-toastify'
import AsyncButton from '../components/AsyncButton'

const AdminUserManagement = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingUser, setEditingUser] = useState(null)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    role: 'regular',
    password: '',
  })

  // Pagination state
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)
  const pageSize = 5

  // IntersectionObserver ref
  const observerRef = useRef(null)

  // Fetch users from the server
  const fetchUsers = async (pageToLoad) => {
    setLoading(true)
    try {
      const response = await axiosInstance.get('/users', {
        params: { page: pageToLoad, size: pageSize },
      })
      // Defensive parse: check response.data?.data, or if response.data is an array, otherwise empty
      const newUsers = Array.isArray(response.data?.data)
        ? response.data.data
        : Array.isArray(response.data)
        ? response.data
        : []

      setUsers((prev) => [...prev, ...newUsers])
      // Explicitly set hasMore based on returned count
      setHasMore(newUsers.length === pageSize)
    } catch (err) {
      setError('Failed to load users')
      toast.error('Failed to load users', { autoClose: 15000 })
    } finally {
      setLoading(false)
    }
  }

  // Initial fetch on mount
  useEffect(() => {
    fetchUsers(page)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // IntersectionObserver callback for infinite scroll
  const lastUserRef = useCallback(
    (node) => {
      if (loading || !hasMore) return
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
      observerRef.current = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          const nextPage = page + 1
          setPage(nextPage)
          fetchUsers(nextPage)
        }
      })
      if (node) observerRef.current.observe(node)
    },
    [loading, hasMore, page]
  )

  // Manual "Load More" fallback button handler
  const loadMore = () => {
    if (loading || !hasMore) return
    const nextPage = page + 1
    setPage(nextPage)
    fetchUsers(nextPage)
  }

  // Create or update user
  const handleCreateOrUpdate = async (e) => {
    e.preventDefault()
    if (editingUser) {
      try {
        // Remove empty password field for updates
        const updateData = { ...formData }
        if (!updateData.password || updateData.password.trim() === '') {
          delete updateData.password
        }
        const response = await axiosInstance.put(`/users/${editingUser._id}`, updateData)
        toast.success('User updated successfully', { autoClose: 2000 })
        // Update the user in the list with returned data
        if (response.data?.user) {
          setUsers((prev) =>
            prev.map((u) => (u._id === editingUser._id ? { ...response.data.user, _id: editingUser._id } : u))
          )
        } else {
          // Fallback: refresh the list
          setUsers([])
          setPage(1)
          setHasMore(true)
          fetchUsers(1)
        }
        setEditingUser(null)
        setShowForm(false)
        setFormData({ username: '', email: '', role: 'regular', password: '' })
      } catch (err) {
        const errorMsg = err.response?.data?.error || err.response?.data?.message || 'Failed to update user'
        toast.error(errorMsg, { autoClose: false })
      }
    } else {
      try {
        const response = await axiosInstance.post('/users', formData)
        toast.success('User created successfully', { autoClose: 2000 })
        // Clear the list and re-fetch from page 1.
        setUsers([])
        setPage(1)
        setHasMore(true)
        setShowForm(false)
        setFormData({ username: '', email: '', role: 'regular', password: '' })
        fetchUsers(1)
      } catch (err) {
        toast.error('Failed to create user', { autoClose: 15000 })
      }
    }
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleDelete = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await axiosInstance.delete(`/users/${userId}`)
        toast.success('User deleted successfully', { autoClose: 2000 })
        setUsers((prev) => prev.filter((u) => u._id !== userId))
      } catch (err) {
        toast.error('Failed to delete user', { autoClose: false })
      }
    }
  }

  const startEdit = (user) => {
    setEditingUser(user)
    setFormData({
      username: user.username,
      email: user.email,
      role: user.role || 'regular',
      password: '',
    })
    setShowForm(true)
  }

  return (
    <div className="p-8">
      {error && <div className="text-red-600">{error}</div>}
      <h2 className="text-2xl font-bold mb-4">Admin User Management</h2>

      {!showForm && (
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded mb-4"
          onClick={() => {
            setShowForm(true)
            setEditingUser(null)
            setFormData({ username: '', email: '', role: 'regular', password: '' })
          }}
        >
          Create New User
        </button>
      )}

      {showForm && (
        <form onSubmit={handleCreateOrUpdate} autoComplete="off" className="mt-4 p-4 border rounded max-w-md">
          <h3 className="text-xl font-semibold mb-2">
            {editingUser ? 'Edit User' : 'Create User'}
          </h3>
          <div className="mb-2">
            <label htmlFor="username" className="block mb-1">
              Username
            </label>
            <input
              id="username"
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="border p-2 w-full"
              required
              autoComplete="off"
            />
          </div>
          <div className="mb-2">
            <label htmlFor="email" className="block mb-1">
              Email
            </label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="border p-2 w-full"
              required
              autoComplete="off"
            />
          </div>
          <div className="mb-2">
            <label htmlFor="role" className="block mb-1">
              Role
            </label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="border p-2 w-full"
              autoComplete="off"
            >
              <option value="admin">Admin</option>
              <option value="moderator">Moderator</option>
              <option value="regular">Regular</option>
            </select>
          </div>
          {!editingUser && (
            <div className="mb-2">
              <label htmlFor="password" className="block mb-1">
                Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="border p-2 w-full"
                required
                autoComplete="new-password"
              />
            </div>
          )}
          <div className="flex space-x-2 mt-4">
            <AsyncButton
              type="submit"
              initialLabel={editingUser ? 'Update User' : 'Create User'}
              loadingLabel={editingUser ? 'Updating...' : 'Creating...'}
              onClick={handleCreateOrUpdate}
              className="bg-blue-600 text-white px-4 py-2 rounded"
            />
            <button
              type="button"
              className="bg-gray-600 text-white px-4 py-2 rounded"
              onClick={() => setShowForm(false)}
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      <div className="overflow-y-auto" style={{ maxHeight: '400px' }}>
        <table className="w-full border-collapse">
          <thead>
            <tr>
              <th className="border p-2">Username</th>
              <th className="border p-2">Email</th>
              <th className="border p-2">Role</th>
              <th className="border p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, idx) => {
              const isLastRow = idx === users.length - 1
              return (
                <tr key={user._id} data-testid="user-row" ref={isLastRow ? lastUserRef : null}>
                  <td className="border p-2">{user.username}</td>
                  <td className="border p-2">{user.email}</td>
                  <td className="border p-2">{user.role}</td>
                  <td className="border p-2">
                    <button
                      className="mr-2 bg-yellow-500 text-white px-2 py-1 rounded"
                      onClick={() => startEdit(user)}
                    >
                      Edit
                    </button>
                    <button
                      className="bg-red-500 text-white px-2 py-1 rounded"
                      onClick={() => handleDelete(user._id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {loading && <div>Loading...</div>}
        {!hasMore && (
          <div className="mt-2 text-gray-500">No more users to load</div>
        )}
      </div>

      {/* Always render the "Load More" button */}
      <button
        className="mt-4 bg-green-600 text-white px-4 py-2 rounded"
        onClick={loadMore}
        disabled={loading || !hasMore}
      >
        {loading ? 'Loading...' : hasMore ? 'Load More' : 'No More Users'}
      </button>
    </div>
  )
}

export default AdminUserManagement
