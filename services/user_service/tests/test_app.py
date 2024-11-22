import unittest
from flask import json
from services.user_service.app import app
from data.users import UserDatabase

# Initialize your user database instance
user_db = UserDatabase()

class UserServiceTestCase(unittest.TestCase):

    TEST_USER_SUFFIX = "@test.com"  # Unique email suffix to identify test users

    @classmethod
    def setUpClass(cls):
        """Setup the Flask test client once for the test suite."""
        cls.client = app.test_client()

    def register_user(self, name, email, password, role, admin_secret_key=None):
        """Helper function to register a user."""
        data = {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }

        if admin_secret_key:
            data['admin_secret_key'] = admin_secret_key

        return self.client.post('/register', data=json.dumps(data), content_type='application/json')

    def login_user(self, email, password):
        """Helper function to login a user."""
        data = {
            "email": email,
            "password": password
        }
        return self.client.post('/login', data=json.dumps(data), content_type='application/json')

    def get_jwt_token(self, email, password):
        """Helper function to get a JWT token."""
        response = self.login_user(email, password)
        data = json.loads(response.data)
        if response.status_code == 200 and 'token' in data:
            return data['token']
        return None

    def tearDown(self):
        """Tear down method to delete test users after each test."""
        # Remove only test users that have the TEST_USER_SUFFIX in their email.
        self._remove_test_users()

    def _remove_test_users(self):
        """Helper method to remove test users from the database."""
        users = user_db._load_users()
        users = {uid: user for uid, user in users.items() if not user['email'].endswith(self.TEST_USER_SUFFIX)}
        user_db._save_users(users)

    def test_register_user_success(self):
        """Test successful user registration."""
        response = self.register_user('Test User', f'testuser{self.TEST_USER_SUFFIX}', 'password123', 'User')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertIn('user_id', data)

    def test_register_missing_fields(self):
        """Test registration with missing fields."""
        response = self.client.post('/register', data=json.dumps({
            "name": "Test User"
        }), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing required fields: email, password, role')

    def test_register_invalid_email(self):
        """Test registration with an invalid email format."""
        response = self.register_user('Test User', 'invalid-email', 'password123', 'User')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid email format')

    def test_register_admin_without_key(self):
        """Test admin registration without admin secret key."""
        response = self.register_user('Admin User', f'adminuser{self.TEST_USER_SUFFIX}', 'password123', 'Admin')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Admin secret key is required for admin registration')

    def test_register_admin_with_invalid_key(self):
        """Test admin registration with an invalid admin secret key."""
        response = self.register_user('Admin User', f'adminuser{self.TEST_USER_SUFFIX}', 'password123', 'Admin', admin_secret_key='wrong_key')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid admin secret key')

    def test_login_success(self):
        """Test successful login."""
        # Register a test user
        self.register_user('Login User', f'loginuser{self.TEST_USER_SUFFIX}', 'password123', 'User')

        # Test login
        response = self.login_user(f'loginuser{self.TEST_USER_SUFFIX}', 'password123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertIn('token', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.login_user('nonexistent@example.com', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid credentials')

    # Additional tests...

    def test_register_invalid_email(self):
        """Test registration with an invalid email format."""
        response = self.register_user('Test User', 'invalid-email', 'password123', 'User')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid email format')

    def test_register_admin_without_key(self):
        """Test admin registration without admin secret key."""
        response = self.register_user('Admin User', 'admin@example.com', 'password123', 'Admin')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Admin secret key is required for admin registration')

    def test_register_admin_with_invalid_key(self):
        """Test admin registration with an invalid admin secret key."""
        response = self.register_user('Admin User', 'admin@example.com', 'password123', 'Admin', admin_secret_key='wrong_key')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid admin secret key')

    def test_login_success(self):
        """Test successful login."""
        # Register a test user
        self.register_user('Login User', 'loginuser@example.com', 'password123', 'User')

        # Test login
        response = self.login_user('loginuser@example.com', 'password123')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertIn('token', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.login_user('nonexistent@example.com', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_get_profile_unauthorized(self):
        """Test access to profile endpoint without a valid token."""
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_profile_with_valid_user_token(self):
        """Test access to the profile endpoint with a valid user token."""
        # Register and login a test user
        self.register_user('Profile User', 'profileuser@example.com', 'password123', 'User')
        token = self.get_jwt_token('profileuser@example.com', 'password123')

        # Access profile with valid user token
        response = self.client.get('/profile', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Profile User')

    def test_get_profile_with_admin_token(self):
        """Test access to the profile endpoint with a valid admin token to fetch all profiles."""
        # Register and login an admin user
        self.register_user('Admin User', 'adminprofile@example.com', 'adminpass', 'Admin', admin_secret_key='your_admin_secret_key_here')
        token = self.get_jwt_token('adminprofile@example.com', 'adminpass')

        # Access profile with valid admin token
        response = self.client.get('/profile', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)  # Admin should get a list of all users
        self.assertGreater(len(data), 0)
        self.assertTrue(any(user['name'] == 'Admin User' for user in data))


if __name__ == '__main__':
    unittest.main()
