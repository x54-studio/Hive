# C4 Level 4: Code-Level Details

## Overview

This document provides code-level details and references to key implementation files in the Hive system. It focuses on critical code patterns, architectural decisions, and implementation details.

---

## Backend Code Structure

### Application Factory Pattern

**File**: `backend/app/__init__.py`

The application factory pattern allows for:
- Modular app creation
- Easy testing (multiple app instances)
- Configuration flexibility

**Key Implementation**:
```python
def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Register blueprints, error handlers, etc.
    return app
```

### Repository Pattern

**Base Interface**: `backend/repositories/base_user_repository.py`  
**Implementation**: `backend/repositories/mongo_user_repository.py`

The repository pattern abstracts data access:

**Base Interface**:
```python
class BaseUserRepository(ABC):
    @abstractmethod
    def create_user(self, user_data: dict) -> str:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[dict]:
        pass
```

**MongoDB Implementation**:
```python
class MongoUserRepository(BaseUserRepository):
    def __init__(self, db):
        self.collection = db.users
    
    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
```

**Benefits**:
- Easy to swap MongoDB for PostgreSQL/SQLite
- Testable (mock repositories)
- Clear separation of concerns

### Service Layer Pattern

**File**: `backend/services/user_service.py`

Services contain business logic, separate from API and data layers:

**Example**:
```python
class UserService:
    def __init__(self, user_repo: BaseUserRepository):
        self.user_repo = user_repo
    
    def register_user(self, user_data: dict) -> dict:
        # Business logic: validation, password hashing
        if self.user_repo.find_by_email(user_data['email']):
            raise UserAlreadyExistsException()
        
        user_data['password'] = bcrypt.hashpw(
            user_data['password'].encode('utf-8'),
            bcrypt.gensalt()
        )
        
        user_id = self.user_repo.create_user(user_data)
        return {'user_id': user_id}
```

**Benefits**:
- Reusable business logic
- Testable without HTTP layer
- Single responsibility principle

### JWT Token Management

**File**: `backend/app/__init__.py` (JWT configuration)  
**File**: `backend/services/user_service.py` (Token generation)

**Token Generation**:
```python
from flask_jwt_extended import create_access_token, create_refresh_token

access_token = create_access_token(
    identity=user_id,
    additional_claims={'role': user_role}
)

refresh_token = create_refresh_token(identity=user_id)
```

**Cookie Configuration**:
```python
response.set_cookie(
    'access_token',
    access_token,
    httponly=True,
    secure=True,  # HTTPS only
    samesite='Strict',
    max_age=900  # 15 minutes
)
```

### Error Handling

**File**: `backend/app/error_handlers.py`

Centralized error handling ensures consistent responses:

```python
@app.errorhandler(CustomException)
def handle_custom_exception(e):
    logger.error(f"Error: {e.message}")
    return jsonify({'error': e.message}), e.status_code

@app.errorhandler(500)
def handle_internal_error(e):
    logger.error(f"Internal error: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500
```

**Security**: Internal error details are logged but not exposed to clients.

### Input Validation (Pydantic)

**File**: `backend/app/routes/user_routes.py`

Pydantic schemas validate all request payloads:

```python
from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    class Config:
        min_anystr_length = 1

@user_routes.route('/register', methods=['POST'])
def register():
    data = RegisterSchema(**request.json)
    # data is validated and typed
```

---

## Frontend Code Structure

### Redux Toolkit State Management

**File**: `frontend/src/redux/slices/authSlice.js`

**Slice Definition**:
```javascript
const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  },
  reducers: {
    logout: (state) => {
      state.user = null
      state.isAuthenticated = false
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true
      })
      .addCase(login.fulfilled, (state, action) => {
        state.user = action.payload
        state.isAuthenticated = true
        state.loading = false
      })
  }
})
```

**Async Thunk**:
```javascript
export const login = createAsyncThunk(
  'auth/login',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await axios.post('/api/login', credentials, {
        credentials: 'include'
      })
      return response.data
    } catch (error) {
      return rejectWithValue(error.response.data)
    }
  }
)
```

### Axios Interceptors

**File**: `frontend/src/api/axiosInstance.js`

**Request Interceptor**:
```javascript
axiosInstance.interceptors.request.use(
  (config) => {
    // Access token is automatically sent via HttpOnly cookies
    return config
  },
  (error) => Promise.reject(error)
)
```

**Response Interceptor** (Token Refresh):
```javascript
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        // Attempt token refresh
        await axiosInstance.post('/api/refresh', {}, {
          credentials: 'include'
        })
        // Retry original request
        return axiosInstance.request(error.config)
      } catch (refreshError) {
        // Refresh failed, logout user
        store.dispatch(logout())
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)
```

### Protected Route Component

**File**: `frontend/src/components/ProtectedRoute.js`

**Implementation**:
```javascript
const ProtectedRoute = () => {
  const { isAuthenticated } = useSelector((state) => state.auth)
  
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />
}
```

**Usage**:
```javascript
<Route element={<ProtectedRoute />}>
  <Route path="/profile" element={<Profile />} />
</Route>
```

### Session Management

**File**: `frontend/src/components/SessionManager.js`

**Multi-tab Coordination**:
```javascript
useEffect(() => {
  const handleStorageChange = (e) => {
    if (e.key === 'token_refresh') {
      // Another tab refreshed token, update this tab
      dispatch(refreshUser())
    }
  }
  
  window.addEventListener('storage', handleStorageChange)
  return () => window.removeEventListener('storage', handleStorageChange)
}, [dispatch])
```

**Proactive Token Refresh**:
```javascript
useEffect(() => {
  const refreshInterval = setInterval(() => {
    if (isAuthenticated) {
      refreshToken()
    }
  }, 14 * 60 * 1000) // Refresh every 14 minutes (before 15min expiry)
  
  return () => clearInterval(refreshInterval)
}, [isAuthenticated])
```

### Role-Based Access Control (RBAC)

**File**: `frontend/src/components/Navbar.js`

**Role-Based Rendering**:
```javascript
const { user } = useSelector((state) => state.auth)
const isAdmin = user?.role === 'admin'
const isModerator = user?.role === 'moderator' || isAdmin

return (
  <nav>
    {isModerator && <Link to="/articles/create">Create Article</Link>}
    {isAdmin && <Link to="/admin/users">Admin Panel</Link>}
  </nav>
)
```

**Backend RBAC**:
```python
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function
```

---

## Key Design Decisions

### Why HttpOnly Cookies?

- **Security**: Prevents XSS attacks (JavaScript cannot access cookies)
- **Automatic**: Browser handles cookie sending/receiving
- **No Manual Management**: No need to store tokens in localStorage or state

### Why Repository Pattern?

- **Testability**: Easy to mock repositories in tests
- **Flexibility**: Can swap MongoDB for PostgreSQL without changing services
- **Clean Architecture**: Dependency inversion principle

### Why Redux Toolkit?

- **Predictable State**: Single source of truth
- **DevTools**: Excellent debugging experience
- **Middleware**: Easy to add logging, persistence, etc.
- **TypeScript Support**: Better type safety (if migrated)

### Why Axios Interceptors?

- **Centralized Logic**: Token refresh logic in one place
- **Automatic**: No need to handle 401 in every component
- **Consistent**: All requests benefit from refresh logic

---

## Testing Patterns

### Backend Unit Tests

**File**: `backend/tests/test_user_service.py`

```python
def test_register_user_success(mock_user_repo):
    service = UserService(mock_user_repo)
    result = service.register_user({
        'username': 'test',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert result['user_id'] is not None
    mock_user_repo.create_user.assert_called_once()
```

### Frontend Component Tests

**File**: `frontend/src/__tests__/authSlice.test.js`

```javascript
describe('authSlice', () => {
  it('should handle login success', async () => {
    const dispatch = jest.fn()
    await login({ username: 'test', password: 'pass' })(dispatch)
    
    expect(dispatch).toHaveBeenCalledWith(
      expect.objectContaining({ type: 'auth/login/fulfilled' })
    )
  })
})
```

---

## Code References

### Backend

- **Application Factory**: `backend/app/__init__.py`
- **Routes**: `backend/app/routes/user_routes.py`, `backend/app/routes/article_routes.py`
- **Services**: `backend/services/user_service.py`, `backend/services/article_service.py`
- **Repositories**: `backend/repositories/mongo_user_repository.py`, `backend/repositories/mongo_article_repository.py`
- **Error Handlers**: `backend/app/error_handlers.py`
- **Config**: `backend/app/config.py`
- **Utilities**: `backend/utilities/logger.py`, `backend/utilities/custom_exceptions.py`

### Frontend

- **App Root**: `frontend/src/App.js`
- **Redux Store**: `frontend/src/redux/store.js`
- **Auth Slice**: `frontend/src/redux/slices/authSlice.js`
- **API Client**: `frontend/src/api/axiosInstance.js`
- **Protected Route**: `frontend/src/components/ProtectedRoute.js`
- **Session Manager**: `frontend/src/components/SessionManager.js`
- **Pages**: `frontend/src/pages/Login.js`, `frontend/src/pages/Profile.js`, etc.

---

## Performance Considerations

### Backend

- **Database Indexing**: MongoDB indexes on `email`, `username` for fast lookups
- **Connection Pooling**: MongoDB client connection pooling
- **Pagination**: Backend-enforced pagination to limit response size

### Frontend

- **Code Splitting**: React Router lazy loading (if implemented)
- **Memoization**: React.memo for expensive components
- **Debouncing**: Search input debouncing to reduce API calls

---

## Security Implementation Details

### Password Hashing

**Backend**: `backend/services/user_service.py`

```python
import bcrypt

hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
# Stored in database, never plain text
```

### Rate Limiting

**Backend**: Flask-Limiter configuration

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

@limiter.limit("5 per minute")
@user_routes.route('/login', methods=['POST'])
def login():
    # Stricter limit on auth endpoints
```

### Security Headers

**Backend**: `backend/app/__init__.py`

```python
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
```

---

## Conclusion

This code-level documentation provides insight into the implementation details of the Hive system. For architectural overview, refer to:
- **C4 Level 1**: System Context (`01-system-context.md`)
- **C4 Level 2**: Containers (`02-containers.md`)
- **C4 Level 3**: Components (`03-components-backend.md`, `03-components-frontend.md`)

For API usage, refer to `api-reference.md`.
