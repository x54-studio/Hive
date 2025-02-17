# utilities/custom_exceptions.py
class RepositoryError(Exception):
    """Exception raised for errors in the repository layer."""


class ServiceError(Exception):
    """Exception raised for errors in the service layer."""
