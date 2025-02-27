module.exports = {
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest"
  },
  transformIgnorePatterns: [
    "/node_modules/(?!react-router-dom|axios)"
  ],
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
  testEnvironment: "jsdom",
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "identity-obj-proxy"
  },
  //moduleDirectories: ["node_modules", "src"],
  //extensionsToTreatAsEsm: [".jsx", ".ts", ".tsx"]
};
