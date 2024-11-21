# services/auth_service/auth.py
import jwt
from functools import wraps
from flask import request, jsonify
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.users import UserDatabase

SECRET_KEY = 'your_secret_key_here'
user_db = UserDatabase()

def authenticate_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            
            # Verify user exists
            user = user_db.get_user_by_id(payload['user_id'])
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Pass the current user info to the route
            current_user = {
                'user_id': payload['user_id'],
                'role': payload['role']
            }
            
            return f(current_user, *args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function

def is_admin(f):
    @wraps(f)
    def decorated_function(current_user, *args, **kwargs):
        if current_user['role'] != 'Admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decorated_function