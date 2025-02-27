// src/hooks/useUserRole.js
import { useSelector } from "react-redux";

const useUserRole = () => {
  // Retrieve the user object from the auth slice in the Redux store.
  const user = useSelector((state) => state.auth.user);
  // Return the role if it exists, otherwise undefined.
  return user?.claims?.role;
};

export default useUserRole;
