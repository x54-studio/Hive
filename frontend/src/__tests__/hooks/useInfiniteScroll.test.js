// src/__tests__/useInfiniteScroll.test.js
import React from "react";
import { renderHook } from "@testing-library/react";
import { useInfiniteScroll } from "../../hooks/useInfiniteScroll";

describe("useInfiniteScroll hook", () => {
  test("returns a function for setting up observer", () => {
    const callback = jest.fn();
    const { result } = renderHook(() => useInfiniteScroll(callback));
    expect(typeof result.current).toBe("function");
  });
});
