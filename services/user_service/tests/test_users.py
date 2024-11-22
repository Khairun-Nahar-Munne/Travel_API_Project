# services/user_service/tests/test_users.py
import unittest
from unittest.mock import Mock, patch
from services.user_service.users import UserManager


class TestUserManager(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.user_manager = UserManager()
        self.test_user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'test123',
            'role': 'User'
        }

    def test_hash_password(self):
        """Test password hashing"""
        password = "test123"
        hashed1 = self.user_manager.hash_password(password)
        hashed2 = self.user_manager.hash_password(password)
        self.assertEqual(hashed1, hashed2)
        self.assertNotEqual(hashed1, password)

    @patch('services.user_service.users.UserDatabase')
    def test_register_user_success(self, mock_db):
        """Test successful user registration"""
        # Setup mock
        mock_db.return_value.get_user_by_email.return_value = None
        self.user_manager.user_db = mock_db.return_value

        # Test registration
        user_id = self.user_manager.register_user(
            self.test_user['name'],
            self.test_user['email'],
            self.test_user['password']
        )

        # Assertions
        self.assertIsNotNone(user_id)
        mock_db.return_value.add_user.assert_called_once()
        args = mock_db.return_value.add_user.call_args[0][0]
        self.assertEqual(args['name'], self.test_user['name'])
        self.assertEqual(args['email'], self.test_user['email'])
        self.assertEqual(args['role'], 'User')

    @patch('services.user_service.users.UserDatabase')
    def test_register_user_duplicate_email(self, mock_db):
        """Test registration with duplicate email"""
        # Setup mock to simulate existing user
        mock_db.return_value.get_user_by_email.return_value = {'email': self.test_user['email']}
        self.user_manager.user_db = mock_db.return_value

        # Test registration
        user_id = self.user_manager.register_user(
            self.test_user['name'],
            self.test_user['email'],
            self.test_user['password']
        )

        # Assertions
        self.assertIsNone(user_id)
        mock_db.return_value.add_user.assert_not_called()

    @patch('services.user_service.users.UserDatabase')
    def test_authenticate_user_success(self, mock_db):
        """Test successful user authentication"""
        # Setup mock
        hashed_password = self.user_manager.hash_password(self.test_user['password'])
        mock_user = {**self.test_user, 'password': hashed_password}
        mock_db.return_value.get_user_by_email.return_value = mock_user
        self.user_manager.user_db = mock_db.return_value

        # Test authentication
        user = self.user_manager.authenticate_user(
            self.test_user['email'],
            self.test_user['password']
        )

        # Assertions
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], self.test_user['email'])

    @patch('services.user_service.users.UserDatabase')
    def test_authenticate_user_wrong_password(self, mock_db):
        """Test authentication with wrong password"""
        # Setup mock
        hashed_password = self.user_manager.hash_password(self.test_user['password'])
        mock_user = {**self.test_user, 'password': hashed_password}
        mock_db.return_value.get_user_by_email.return_value = mock_user
        self.user_manager.user_db = mock_db.return_value

        # Test authentication with wrong password
        user = self.user_manager.authenticate_user(
            self.test_user['email'],
            'wrong_password'
        )

        # Assertions
        self.assertIsNone(user)

    @patch('services.user_service.users.UserDatabase')
    def test_get_user_profile(self, mock_db):
        """Test getting user profile"""
        # Setup mock
        mock_user = {
            'id': '123',
            **self.test_user,
            'password': 'hashed_password'
        }
        mock_db.return_value.get_user_by_id.return_value = mock_user
        self.user_manager.user_db = mock_db.return_value

        # Test getting profile
        profile = self.user_manager.get_user_profile('123')

        # Assertions
        self.assertIsNotNone(profile)
        self.assertEqual(profile['name'], self.test_user['name'])
        self.assertEqual(profile['email'], self.test_user['email'])
        self.assertNotIn('password', profile)

    @patch('services.user_service.users.UserDatabase')
    def test_get_all_users(self, mock_db):
        """Test getting all users"""
        # Setup mock
        mock_users = [
            {'id': '1', **self.test_user, 'password': 'hashed_1'},
            {'id': '2', 'name': 'User 2', 'email': 'user2@example.com', 'role': 'User', 'password': 'hashed_2'}
        ]
        mock_db.return_value.get_all_users.return_value = mock_users
        self.user_manager.user_db = mock_db.return_value

        # Test getting all users
        users = self.user_manager.get_all_users()

        # Assertions
        self.assertEqual(len(users), 2)
        self.assertNotIn('password', users[0])
        self.assertNotIn('password', users[1])