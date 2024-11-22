import unittest
from unittest.mock import patch, MagicMock
from services.auth_service.auth import authenticate_token, is_admin
from flask import Flask, jsonify
import jwt

# Setup a simple Flask application for testing
app = Flask(__name__)
app.config['TESTING'] = True
SECRET_KEY = 'your_secret_key_here'

# Dummy user data
dummy_user = {
    'user_id': 1,
    'role': 'Admin'
}

# Dummy token
valid_token = jwt.encode({'user_id': 1, 'role': 'Admin'}, SECRET_KEY, algorithm='HS256')
expired_token = jwt.encode({'user_id': 1, 'role': 'Admin', 'exp': 0}, SECRET_KEY, algorithm='HS256')  # Immediate expiration
invalid_token = 'invalid.token.string'

# Mock database behavior
class MockUserDatabase:
    def get_user_by_id(self, user_id):
        if user_id == 1:
            return dummy_user
        return None

# Apply patches to replace the real UserDatabase with MockUserDatabase
@patch('services.auth_service.auth.user_db', new_callable=lambda: MockUserDatabase())
class AuthServiceTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()

    @app.route('/protected')
    @authenticate_token
    def protected_route(current_user):
        return jsonify({'message': 'Access granted', 'user_id': current_user['user_id']}), 200

    @app.route('/admin')
    @authenticate_token
    @is_admin
    def admin_route(current_user):
        return jsonify({'message': 'Admin access granted'}), 200

    # Test case for valid token
    def test_authenticate_token_valid(self, mock_db):
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access granted', response.get_json()['message'])

    # Test case for missing token
    def test_authenticate_token_missing(self, mock_db):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Authentication token is missing', response.get_json()['error'])

    # Test case for expired token
    def test_authenticate_token_expired(self, mock_db):
        headers = {'Authorization': f'Bearer {expired_token}'}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token has expired', response.get_json()['error'])

    # Test case for invalid token
    def test_authenticate_token_invalid(self, mock_db):
        headers = {'Authorization': f'Bearer {invalid_token}'}
        response = self.client.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid token', response.get_json()['error'])

    # Test case for admin access with valid admin token
    def test_is_admin_valid(self, mock_db):
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = self.client.get('/admin', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Admin access granted', response.get_json()['message'])

    # Test case for admin access with non-admin role
    def test_is_admin_invalid_role(self, mock_db):
        # Non-admin token
        non_admin_token = jwt.encode({'user_id': 1, 'role': 'User'}, SECRET_KEY, algorithm='HS256')
        headers = {'Authorization': f'Bearer {non_admin_token}'}
        response = self.client.get('/admin', headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Admin access required', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()
