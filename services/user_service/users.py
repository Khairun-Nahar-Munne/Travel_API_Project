# services/user_service/users.py
import uuid
import hashlib
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.users import UserDatabase

class UserManager:
    def __init__(self):
        self.user_db = UserDatabase()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, name, email, password, role='User'):
        # Check if email already exists
        if self.user_db.get_user_by_email(email):
            return None

        user_id = str(uuid.uuid4())
        hashed_password = self.hash_password(password)
        
        user = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': role
        }
        
        self.user_db.add_user(user)
        return user_id

    def authenticate_user(self, email, password):
        user = self.user_db.get_user_by_email(email)
        if user and user['password'] == self.hash_password(password):
            return user
        return None

    def get_user_profile(self, user_id):
        user = self.user_db.get_user_by_id(user_id)
        if user:
            # Remove sensitive information before returning
            return {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        return None

    def get_all_users(self):
        # Returns all users (for admin access)
        users = self.user_db.get_all_users()
        return [
            {
                'id': user['id'],
                'name': user['name'], 
                'email': user['email'], 
                'role': user['role']
            } for user in users
        ]