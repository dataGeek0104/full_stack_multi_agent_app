import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders Langchain link", () => {
  render(<App />);
  const linkElement = screen.getByText(/Langchain/i);
  expect(linkElement).toBeInTheDocument();
});
