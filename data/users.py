# data/users.py
import os

class UserDatabase:
    def __init__(self, filename='users_data.py'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self._initialize_database()

    def _initialize_database(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("users = {}")

    def _load_users(self):
        with open(self.filename, 'r') as f:
            exec(f.read())
        return locals()['users']

    def _save_users(self, users):
        with open(self.filename, 'w') as f:
            f.write(f"users = {repr(users)}")

    def add_user(self, user):
        users = self._load_users()
        users[user['id']] = user
        self._save_users(users)

    def get_user_by_id(self, user_id):
        users = self._load_users()
        return users.get(user_id)

    def get_user_by_email(self, email):
        users = self._load_users()
        for user in users.values():
            if user['email'] == email:
                return user
        return None