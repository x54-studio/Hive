import React from "react";

export const Link = ({ children, ...props }) => <a {...props}>{children}</a>;
export const BrowserRouter = ({ children }) => <div>{children}</div>;
export const MemoryRouter = ({ children }) => <div>{children}</div>;
export const Routes = ({ children }) => <div>{children}</div>;
export const Route = ({ element }) => element;
export const useLocation = () => ({ pathname: "/" });
