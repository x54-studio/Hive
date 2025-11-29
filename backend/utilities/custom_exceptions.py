# utilities/custom_exceptions.py
class RepositoryError(Exception):
    """Exception raised for errors in the repository layer."""


class ServiceError(Exception):
    """Exception raised for errors in the service layer."""


class ArticleNotFoundError(Exception):
    """Exception raised when an article is not found."""


class UserNotFoundError(Exception):
    """Exception raised when a user is not found."""


class ValidationError(Exception):
    """Exception raised for validation errors."""


class UnauthorizedError(Exception):
    """Exception raised when user is not authorized to perform an action."""