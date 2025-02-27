// src/__tests__/Routing.test.js
jest.unmock("react-router-dom");

import React from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route, useLocation } from "react-router-dom";

const LocationDisplay = () => {
  const location = useLocation();
  return <div data-testid="location-display">{location.pathname}</div>;
};

describe("MemoryRouter Routing", () => {
  test("renders initial route", () => {
    render(
      <MemoryRouter initialEntries={["/initial"]}>
        <Routes>
          <Route path="/initial" element={<div>Initial Route</div>} />
        </Routes>
        <LocationDisplay />
      </MemoryRouter>
    );
    expect(screen.getByTestId("location-display").textContent).toBe("/initial");
    expect(screen.getByText("Initial Route")).toBeInTheDocument();
  });
});
