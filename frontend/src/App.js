import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Call the backend API
    fetch("http://127.0.0.1:5000/") // Backend URL
      .then((response) => response.json())
      .then((data) => {
        setMessage(data.message); // Assuming the backend sends { "message": "Backend is running!" }
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []); // Empty dependency array ensures it runs once on component mount.

  return (
    <div className="App">
      <h1>Hive Frontend</h1>
      <p>Backend Response: {message}</p>
    </div>
  );
}

export default App;
