# app/schemas.py
from pydantic import BaseModel, Field, EmailStr, field_validator


class ArticleCreateSchema(BaseModel):
    """Schema for creating a new article."""
    title: str = Field(..., min_length=1, max_length=200, description="Article title")
    content: str = Field(..., min_length=1, description="Article content")

    @field_validator('title', 'content')
    @classmethod
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace only')
        return v.strip()


class ArticleUpdateSchema(BaseModel):
    """Schema for updating an existing article."""
    title: str | None = Field(None, min_length=1, max_length=200, description="Article title")
    content: str | None = Field(None, min_length=1, description="Article content")

    @field_validator('title', 'content', mode='before')
    @classmethod
    def validate_not_empty_if_provided(cls, v):
        if v is not None and (not v or not str(v).strip()):
            raise ValueError('Field cannot be empty or whitespace only if provided')
        return v.strip() if v and isinstance(v, str) else v


class UserRegisterSchema(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, max_length=100, description="User password")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v or not v.strip():
            raise ValueError('Username cannot be empty or whitespace only')
        return v.strip()


class UserLoginSchema(BaseModel):
    """Schema for user login."""
    username_or_email: str = Field(..., min_length=1, description="Username or email")
    password: str = Field(..., min_length=1, description="User password")


class UserUpdateSchema(BaseModel):
    """Schema for updating user information."""
    username: str | None = Field(None, min_length=3, max_length=50, description="Username")
    email: EmailStr | None = Field(None, description="User email address")
    password: str | None = Field(None, min_length=6, max_length=100, description="User password")
    role: str | None = Field(None, description="User role (admin, moderator, regular)")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v is not None and v.lower() not in ['admin', 'moderator', 'regular']:
            raise ValueError('Role must be one of: admin, moderator, regular')
        return v.lower() if v else v

    @field_validator('username', mode='before')
    @classmethod
    def validate_username_if_provided(cls, v):
        if v is not None and (not v or not str(v).strip()):
            raise ValueError('Username cannot be empty or whitespace only if provided')
        return v.strip() if v and isinstance(v, str) else v

