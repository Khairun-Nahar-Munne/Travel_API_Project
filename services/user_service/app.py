from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os
import sys
import jwt
import datetime
import re

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.user_service.users import UserManager
from services.auth_service.auth import authenticate_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['ADMIN_SECRET_KEY'] = 'your_admin_secret_key_here'

# Initialize User Manager
user_manager = UserManager()

def is_valid_email(email):
    """Validate email format using regex pattern."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

# Swagger Configuration
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "User Service"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'error': 'Request body is required'}), 400

    required_fields = ['name', 'email', 'password', 'role']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    # Validate required fields
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Validate field types and empty values
    for field in required_fields:
        if not isinstance(data[field], str):
            return jsonify({'error': f'{field} must be a string'}), 400
        if not data[field].strip():
            return jsonify({'error': f'{field} cannot be empty'}), 400
            
    # Validate email format
    if not is_valid_email(data['email'].strip()):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Check if role is valid
    if data['role'] not in ['User', 'Admin']:
        return jsonify({'error': 'Invalid role. Must be either User or Admin'}), 400
    
    # If registering as Admin, check for admin secret key in request body
    if data['role'] == 'Admin':
        admin_secret = data.get('admin_secret_key')
        if not admin_secret:
            return jsonify({'error': 'Admin secret key is required for admin registration'}), 401
        if not isinstance(admin_secret, str) or admin_secret != app.config['ADMIN_SECRET_KEY']:
            return jsonify({'error': 'Invalid admin secret key'}), 403
    
    # Remove admin_secret_key from data before passing to register_user
    if 'admin_secret_key' in data:
        data.pop('admin_secret_key')
    
    user_id = user_manager.register_user(
        data['name'].strip(), 
        data['email'].strip(), 
        data['password'], 
        data['role']
    )
    
    if user_id:
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    return jsonify({'error': 'Email already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    required_fields = ['email', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    # Validate required fields
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Validate field types and empty values
    for field in required_fields:
        if not isinstance(data[field], str):
            return jsonify({'error': f'{field} must be a string'}), 400
        if not data[field].strip():
            return jsonify({'error': f'{field} cannot be empty'}), 400
            
    # Validate email format
    if not is_valid_email(data['email'].strip()):
        return jsonify({'error': 'Invalid email format'}), 400
    
    user = user_manager.authenticate_user(data['email'].strip(), data['password'])
    
    if user:
        # Create JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful', 
            'token': token,
            'role': user['role']
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
@authenticate_token
def get_profile(current_user):
    # Check if the user is an admin or requesting their own profile
    if current_user['role'] == 'Admin':
        profile = user_manager.get_all_users()
    else:
        profile = user_manager.get_user_profile(current_user['user_id'])
    
    if profile:
        return jsonify(profile), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)