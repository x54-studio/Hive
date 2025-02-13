// src/components/Layout.js
import React from "react";

/**
 * Layout component that wraps the entire application.
 * It applies an auto-generated, animated SVG background that scales to full width and height,
 * even on high resolution monitors (e.g., 4096 x 2160).
 */
const Layout = ({ children }) => {
  return (
    <div className="w-full min-h-screen relative">
      {/* Background SVG covering full width and height */}
      <svg
        className="absolute inset-0 w-full h-full"
        viewBox="10 -20 930 600"  // Coordinates that match our design; scales automatically
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
      >
        {/* First organic shape */}
        <path
          d="M0,200 Q250,100 500,200 T1000,200 L1000,600 L0,600 Z"
          opacity="0.3"
          style={{
            animation: "shapeColorShift 30s ease-in-out infinite",
          }}
        />
        {/* Second organic shape */}
        <path
          d="M0,400 Q250,500 500,400 T1000,400 L1000,600 L0,600 Z"
          opacity="0.3"
          style={{
            animation: "shapeColorShift2 45s ease-in-out infinite",
          }}
        />
      </svg>

      {/* Main content container (ensures content is layered above the SVG) */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export default Layout;
