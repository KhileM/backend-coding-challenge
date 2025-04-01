from flask import request, abort
from functools import wraps
from app.config import USER_TOKENS

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            abort(401, description="Missing Authorization header.")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            abort(401, description="Invalid Authorization format. Use 'Bearer <token>'.")

        token = parts[1]

        # Match token to user
        matched_user = next((user for user, user_token in USER_TOKENS.items() if user_token == token), None)

        if not matched_user:
            abort(403, description="Invalid or expired token.")

        # Use body param for POST/PUT, route param for GET
        if request.method == 'GET':
            requested_user = kwargs.get('user_id')
        else:
            requested_user = request.json.get('userId') if request.is_json else None

        # Log debug output to console
        print(f"[DEBUG] matched_user={matched_user} | requested_user={requested_user}")

        if not requested_user or matched_user.lower() != requested_user.lower():
            abort(403, description="You can only access your own messages.")


        return func(*args, **kwargs)
    return wrapper
