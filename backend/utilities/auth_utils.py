# backend/utilities/auth_utils.py
from flask import make_response


def set_auth_cookies(response, tokens, config):
    """
    Centralized cookie setting logic for authentication tokens.
    
    Args:
        response: Flask response object
        tokens: Dict with 'access_token' and 'refresh_token' keys
        config: Config object with cookie settings
        
    Returns:
        Flask response object with cookies set
    """
    same_site = config.COOKIE_SAMESITE
    secure = config.FLASK_ENV == "production"
    
    response.set_cookie(
        "access_token",
        tokens["access_token"],
        httponly=True,
        max_age=int(config.JWT_ACCESS_TOKEN_EXPIRES),
        samesite=same_site,
        secure=secure,
        path="/"
    )
    response.set_cookie(
        "refresh_token",
        tokens["refresh_token"],
        httponly=True,
        max_age=int(config.JWT_REFRESH_TOKEN_EXPIRES),
        samesite=same_site,
        secure=secure,
        path="/"
    )
    return response


def delete_auth_cookies(response, config):
    """
    Centralized cookie deletion logic for authentication tokens.
    
    Args:
        response: Flask response object
        config: Config object with cookie settings
        
    Returns:
        Flask response object with cookies deleted
    """
    same_site = config.COOKIE_SAMESITE
    secure = config.FLASK_ENV == "production"
    
    response.delete_cookie("access_token", samesite=same_site, secure=secure, path="/")
    response.delete_cookie("refresh_token", samesite=same_site, secure=secure, path="/")
    return response

