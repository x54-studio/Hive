import '@testing-library/jest-dom';
import React from "react";
import { render, waitFor, screen } from "@testing-library/react";
import Home from "../pages/Home";
import { AuthContext } from "../AuthContext";

// Mock ArticleList to simplify testing Home page layout
jest.mock("../components/ArticleList", () => () => <div>ArticleList Component</div>);

test("Home page renders heading with correct text and theme classes", async () => {
  const dummyUser = { username: "adminUser", role: "admin" };

  render(
    <AuthContext.Provider value={{ user: dummyUser }}>
      <Home />
    </AuthContext.Provider>
  );

  await waitFor(() =>
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Welcome to Hive")
  );
});
