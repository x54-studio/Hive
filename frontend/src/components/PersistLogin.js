// src/components/PersistLogin.js
import React, { useEffect, useState } from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { refreshUser } from '../redux/slices/authSlice'

const PersistLogin = () => {
  const dispatch = useDispatch()
  const { user, error } = useSelector((state) => state.auth)
  const [persistDone, setPersistDone] = useState(false)

  useEffect(() => {
    // Dispatch refreshUser and mark persist as done when complete
    dispatch(refreshUser())
      .unwrap()
      .catch(() => {})
      .finally(() => setPersistDone(true))
  }, [dispatch])

  // While waiting for refreshUser to complete, display a loading indicator.
  if (!persistDone) {
    return <div>Loading...</div>
  }

  // If persist is done and there's no user, redirect to login.
  if (!user && error) {
    return <Navigate to="/login" replace />
  }

  // Otherwise, render the child routes.
  return <Outlet />
}

export default PersistLogin
