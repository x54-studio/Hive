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
