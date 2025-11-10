import '@testing-library/jest-dom'
import { TextEncoder, TextDecoder } from 'util'

global.TextEncoder = TextEncoder
global.TextDecoder = TextDecoder

global.IntersectionObserver = class {
    constructor(callback, options) {
      // Optionally store the callback and options if needed
    }
    observe() {}
    unobserve() {}
    disconnect() {}
  };
  