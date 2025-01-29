import { render } from "@testing-library/react";
import App from "./App";

test("renders articles heading", () => {
  const { getByText } = render(<App />);
  expect(getByText(/Articles/i)).toBeInTheDocument();
});
