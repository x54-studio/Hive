## New Authentication Flow Using Redux Toolkit

We've transitioned from the legacy AuthContext to a centralized authentication flow managed by Redux Toolkit. Key changes include:

- **authSlice.js:**  
  Located in `src/redux/authSlice.js`, this slice uses `createSlice` and `createAsyncThunk` to manage authentication state. It handles:
  - **Login:** An asynchronous thunk (`login`) sends credentials to the backend and updates state based on the API response.
  - **Logout:** A synchronous action clears the authentication state.
  - **setUser:** An optional synchronous action to manually set user data.

- **Component Updates:**  
  Components such as Login, Profile, and Navbar now use the Redux hooks `useSelector` and `useDispatch` to access and update authentication state. This makes our state management more predictable and easier to test.

- **Benefits:**  
  - Centralized state management with a single source of truth.
  - Improved testability through predictable state transitions.
  - Simplified component logic as authentication state is now managed globally.

For further details, refer to the unit tests in `src/__tests__/authSlice.test.js` which demonstrate the expected behavior of our new auth slice.


## Technology Stack

The frontend stack for Hive includes the following key technologies:

- **React:** Used for building the component-based UI.
- **React Router:** Manages client-side navigation and routing.
- **Redux Toolkit & Redux:** Manages global state, especially for user sessions and complex UI logic.
- **React Query:** Handles asynchronous data fetching and caching for server state.
- **Tailwind CSS:** Provides utility-first styling for a responsive design.
- **Jest & React Testing Library:** Used for unit and integration testing.
- **Cypress:** Provides end-to-end testing capabilities.
- **Axios:** For making HTTP requests to the backend API.
- **Babel & Webpack (or Create React App):** For transpiling and bundling the code.
