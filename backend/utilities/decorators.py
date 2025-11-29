# backend/utilities/decorators.py
from flask import request, jsonify
from pydantic import ValidationError as PydanticValidationError


def validate_request(schema_class):
    """Decorator to validate request JSON against a Pydantic schema."""
    def decorator(f):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if data is None:
                return jsonify({"error": "Request body is required", "message": "Request body is required"}), 400
            try:
                validated_data = schema_class(**data)
                kwargs['validated_data'] = validated_data.model_dump(exclude_none=True)
            except PydanticValidationError as e:
                errors = []
                for error in e.errors():
                    field = '.'.join(str(x) for x in error['loc'])
                    errors.append(f"{field}: {error['msg']}")
                # Determine error message based on missing fields
                error_msg = "Validation failed"
                missing_fields = []
                for error in e.errors():
                    field = '.'.join(str(x) for x in error['loc'])
                    error_type = error.get('type', '')
                    if 'missing' in error_type.lower() or 'required' in error.get('msg', '').lower():
                        missing_fields.append(field)
                if missing_fields:
                    # Check for article fields (title/content)
                    if any(f in ['title', 'content'] for f in missing_fields):
                        error_msg = "Missing title or content"
                    # Check for login fields (username_or_email/password) - only for login schema
                    elif any(f in ['username_or_email'] for f in missing_fields):
                        error_msg = "Missing email or password"
                    # For register, use generic message
                    else:
                        error_msg = "Missing required fields"
                return jsonify({
                    "error": error_msg,
                    "message": "Validation failed",
                    "details": errors
                }), 400
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

