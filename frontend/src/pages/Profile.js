import React from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchProtectedData } from "../api/protected";

const Profile = () => {
  const { data, error, status, isLoading } = useQuery({
    queryKey: ["profile"],
    queryFn: fetchProtectedData,
    staleTime: 5000,
  });

  if (isLoading) return <div>Loading user profile...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h2>User Profile</h2>
      <p>Status: {status}</p>
      <p>Username: {data.username}</p>
      <pre>{JSON.stringify(data.claims, null, 2)}</pre>
    </div>
  );
};

export default Profile;
