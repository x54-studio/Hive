module.exports = {
  useNavigate: () => jest.fn(),
  // Add any other exports that your components might import from react-router-dom
  Link: ({ children, ...props }) => <a {...props}>{children}</a>,
  BrowserRouter: ({ children }) => <div>{children}</div>,
  Routes: ({ children }) => <div>{children}</div>,
  Route: ({ element }) => element,
}
