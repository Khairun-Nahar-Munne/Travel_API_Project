import unittest
import os
import shutil


class TestUserDatabase(unittest.TestCase):
    def setUp(self):
        # Create a test directory and set it up as our working directory for tests
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_db')
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        # Set up the test file path
        self.test_db_file = os.path.join(self.test_dir, 'test_users_data.py')
        
        # Remove any existing test file
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
            
        # Import UserDatabase here to ensure we're using clean state
        from data.users import UserDatabase
        self.db = UserDatabase(self.test_db_file)
        
        # Sample test users
        self.test_user1 = {
            'id': '1',
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        self.test_user2 = {
            'id': '2',
            'name': 'Jane Smith',
            'email': 'jane@example.com'
        }

    def tearDown(self):
        # Clean up the entire test directory
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initialize_database(self):
        """Test if database file is created properly"""
        self.assertTrue(os.path.exists(self.test_db_file), 
                       f"Database file not found at {self.test_db_file}")
        with open(self.test_db_file, 'r') as f:
            content = f.read().strip()
        self.assertEqual(content, "users = {}")

    def test_add_user(self):
        """Test adding a user to the database"""
        self.db.add_user(self.test_user1)
        retrieved_user = self.db.get_user_by_id('1')
        self.assertEqual(retrieved_user, self.test_user1)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        self.db.add_user(self.test_user1)
        self.db.add_user(self.test_user2)
        
        # Test existing user
        user = self.db.get_user_by_id('2')
        self.assertEqual(user, self.test_user2)
        
        # Test non-existent user
        user = self.db.get_user_by_id('999')
        self.assertIsNone(user)

    def test_get_user_by_email(self):
        """Test retrieving a user by email"""
        self.db.add_user(self.test_user1)
        self.db.add_user(self.test_user2)
        
        # Test existing user
        user = self.db.get_user_by_email('jane@example.com')
        self.assertEqual(user, self.test_user2)
        
        # Test non-existent user
        user = self.db.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(user)

    def test_get_all_users(self):
        """Test retrieving all users"""
        self.db.add_user(self.test_user1)
        self.db.add_user(self.test_user2)
        
        users = self.db.get_all_users()
        self.assertEqual(len(users), 2)
        self.assertIn(self.test_user1, users)
        self.assertIn(self.test_user2, users)

    def test_persistence(self):
        """Test if data persists between database instances"""
        # Add user with first instance
        self.db.add_user(self.test_user1)
        
        # Create new instance with same file
        from data.users import UserDatabase
        new_db = UserDatabase(self.test_db_file)
        retrieved_user = new_db.get_user_by_id('1')
        self.assertEqual(retrieved_user, self.test_user1)

    def test_file_corruption_handling(self):
        """Test database behavior with corrupted file"""
        # Create a fresh instance for this test
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)
            
        from data.users import UserDatabase
        self.db = UserDatabase(self.test_db_file)
        
        # Write invalid Python to the database file
        with open(self.test_db_file, 'w') as f:
            f.write("This is not valid Python code")
        
        # Test that corrupted file is handled gracefully
        with self.assertRaises(SyntaxError):
            self.db._load_users()

if __name__ == '__main__':
    unittest.main()