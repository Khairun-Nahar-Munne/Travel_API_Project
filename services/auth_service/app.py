# services/auth_service/app.py
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os
import sys
import jwt

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.auth_service.auth import authenticate_token, SECRET_KEY
from data.users import UserDatabase

app = Flask(__name__)

# Initialize User Database
user_db = UserDatabase()

# Swagger Configuration
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Authentication Service"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/auth/verify', methods=['POST'])
def verify_token():
    """
    Verify the validity of an authentication token
    """
    data = request.json
    
    # Validate input
    if not data or 'token' not in data:
        return jsonify({'error': 'Token is required'}), 400
    
    token = data['token']
    
    try:
        # Attempt to decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Verify user exists
        user = user_db.get_user_by_id(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'valid': True,
            'user_id': payload['user_id'],
            'role': payload['role']
        }), 200
    
    except jwt.ExpiredSignatureError:
        return jsonify({
            'valid': False,
            'error': 'Token has expired'
        }), 401
    
    except jwt.InvalidTokenError:
        return jsonify({
            'valid': False,
            'error': 'Invalid token'
        }), 401

@app.route('/auth/roles', methods=['GET'])
@authenticate_token
def get_user_roles(current_user):
    """
    Retrieve the roles of the current authenticated user
    """
    try:
        user = user_db.get_user_by_id(current_user['user_id'])
        if user:
            return jsonify({
                'user_id': user['id'],
                'role': user['role']
            }), 200
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)