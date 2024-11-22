import unittest
import json
from unittest.mock import patch, MagicMock
import jwt
from datetime import datetime, timedelta, timezone
import sys
import os
from functools import wraps

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from services.auth_service.app import app, SECRET_KEY

class TestAuthService(unittest.TestCase):
    def setUp(self):
        """Set up test client and common test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Test data
        self.test_user = {
            'id': '123',
            'username': 'testuser',
            'role': 'user'
        }
        
        # Create a valid token for testing
        self.valid_token = jwt.encode(
            {
                'user_id': self.test_user['id'],
                'role': self.test_user['role'],
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        
        # Create an expired token for testing
        self.expired_token = jwt.encode(
            {
                'user_id': self.test_user['id'],
                'role': self.test_user['role'],
                'exp': datetime.now(timezone.utc) - timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm='HS256'
        )

    def mock_authenticate_token(self, current_user=None):
        """Mock the authentication decorator to simulate the current user"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                # Simulate authenticated user
                if current_user:
                    kwargs['current_user'] = current_user
                return f(*args, **kwargs)
            return decorated
        return decorator

    def test_swagger_ui(self):
        """Test if Swagger UI endpoint is accessible"""
        response = self.app.get('/docs/')
        self.assertEqual(response.status_code, 200)

    @patch('services.auth_service.app.user_db.get_user_by_id')
    def test_verify_valid_token(self, mock_get_user):
        """Test token verification with valid token"""
        # Mock the user database response
        mock_get_user.return_value = self.test_user
        
        response = self.app.post('/auth/verify',
                               data=json.dumps({'token': self.valid_token}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['valid'])
        self.assertEqual(data['user_id'], self.test_user['id'])
        self.assertEqual(data['role'], self.test_user['role'])
        mock_get_user.assert_called_once()

    def test_verify_missing_token(self):
        """Test token verification with missing token"""
        response = self.app.post('/auth/verify',
                               data=json.dumps({}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Token is required')

    @patch('services.auth_service.app.user_db.get_user_by_id')
    def test_verify_expired_token(self, mock_get_user):
        """Test token verification with expired token"""
        mock_get_user.return_value = self.test_user
        
        response = self.app.post('/auth/verify',
                               data=json.dumps({'token': self.expired_token}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['valid'])
        self.assertEqual(data['error'], 'Token has expired')

    @patch('services.auth_service.app.user_db.get_user_by_id')
    def test_verify_invalid_token(self, mock_get_user):
        """Test token verification with invalid token"""
        mock_get_user.return_value = self.test_user
        
        response = self.app.post('/auth/verify',
                               data=json.dumps({'token': 'invalid-token'}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['valid'])
        self.assertEqual(data['error'], 'Invalid token')

    @patch('services.auth_service.app.user_db.get_user_by_id')
    def test_verify_nonexistent_user(self, mock_get_user):
        """Test token verification with non-existent user"""
        mock_get_user.return_value = None
        
        response = self.app.post('/auth/verify',
                               data=json.dumps({'token': self.valid_token}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()
