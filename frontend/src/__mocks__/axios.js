// frontend/__mocks__/axios.js
const axios = {
    get: jest.fn(() => Promise.resolve({ data: {} })),
    post: jest.fn(() => Promise.resolve({ data: {} })),
    create: jest.fn(() => axios),
  };
  
  module.exports = axios;
  