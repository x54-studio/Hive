// src/hooks/useTokenRefresh.js
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { refreshTokens } from '../redux/authSlice';
// Adjust this import if your jwt‑decode library exports differently.
import { jwtDecode as jwt_decode } from 'jwt-decode';

const useTokenRefresh = () => {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);

  useEffect(() => {
    let timeoutId;
    if (user?.accessToken) {
      try {
        const decoded = jwt_decode(user.accessToken);
        const exp = decoded.exp; // expiration time (in seconds since epoch)
        const currentTime = Date.now() / 1000;
        const timeLeft = exp - currentTime;
        // Refresh a few seconds before the token expires.
        const refreshThreshold = 3; // seconds
        const delay = Math.max((timeLeft - refreshThreshold) * 1000, 0);
        console.log("Scheduling token refresh in", delay, "ms");
        timeoutId = setTimeout(() => {
          dispatch(refreshTokens());
        }, delay);
      } catch (err) {
        console.error("Error decoding token:", err);
      }
    }
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [user, dispatch]);
};

export default useTokenRefresh;
