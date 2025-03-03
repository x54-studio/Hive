// src/components/RBACDemo.js
import React from 'react'
import { useSelector } from 'react-redux'

const RBACDemo = () => {
  const { user } = useSelector((state) => state.auth)

  if (!user) {
    return <div>Please log in.</div>
  }

  switch (user.role) {
    case 'admin':
      return <div>Admin Dashboard</div>
    case 'editor':
      return <div>Editor Panel</div>
    case 'user':
      return <div>User Profile</div>
    default:
      return <div>Unknown Role</div>
  }
}

export default RBACDemo
