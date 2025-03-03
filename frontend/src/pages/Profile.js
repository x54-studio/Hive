// src/pages/Profile.js
import React from 'react'

const Profile = () => {
  return (
    <div className="flex flex-col items-center justify-center pt-40">
      <h2 className="text-3xl font-bold mb-4">Profile Page</h2>
      <p>This is a protected route. Only authenticated users can access this page.</p>
    </div>
  )
}

export default Profile
