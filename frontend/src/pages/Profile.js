import React, { useContext } from "react";
import { AuthContext } from "../AuthContext";

function Profile() {
  const { user, logout } = useContext(AuthContext);

  if (!user) {
    return (
      <p className="text-red-600 dark:text-red-400 text-center mt-8">
        Please log in to view your profile.
      </p>
    );
  }

  return (
    <div className="flex flex-col items-center p-6 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 rounded-lg shadow-md mx-4 my-8">
      <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-gray-200">
        User Profile
      </h2>
      <p className="mb-2">
        <strong>Username:</strong> {user.username || "N/A"}
      </p>
      <p className="mb-4">
        <strong>Role:</strong> {user.role || "N/A"}
      </p>
      <pre className="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-200 p-2 rounded w-full overflow-auto">
        {JSON.stringify(user, null, 2)}
      </pre>
      <button
        onClick={logout}
        className="bg-red-500 text-white px-4 py-2 mt-6 rounded hover:bg-red-600"
      >
        Logout
      </button>
    </div>
  );
}

export default Profile;
