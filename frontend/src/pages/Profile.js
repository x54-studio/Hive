import React, { useContext } from "react";
import { AuthContext } from "../AuthContext";

function Profile() {
  const { user, logout } = useContext(AuthContext);

  if (!user) {
    return <p className="text-red-500">Please log in to view your profile.</p>;
  }

  return (
    <div className="flex flex-col items-center p-6 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold">User Profile</h2>
      <p className="mt-2"><strong>Username:</strong> {user.username || "N/A"}</p>
      <p><strong>Role:</strong> {user.role || "N/A"}</p>
      <pre className="bg-gray-200 text-black p-2 mt-4 rounded">{JSON.stringify(user, null, 2)}</pre> {/* Debugging */}
      <button onClick={logout} className="bg-red-500 text-white px-4 py-2 mt-3 rounded">
        Logout
      </button>
    </div>
  );
}

export default Profile;
