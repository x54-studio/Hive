// src/setupTests.js
import { TextEncoder, TextDecoder } from "util";
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;
import '@testing-library/jest-dom';

// Polyfill for IntersectionObserver for tests
if (typeof IntersectionObserver === 'undefined') {
  class IntersectionObserver {
    constructor(callback, options) {
      // You can store the callback if you need to simulate intersections in your tests.
    }
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  global.IntersectionObserver = IntersectionObserver;
}
