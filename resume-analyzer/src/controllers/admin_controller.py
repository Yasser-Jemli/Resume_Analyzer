from flask import Blueprint
from ..models.database import Database

db = Database()

admin_bp = Blueprint('admin', __name__)

class AdminController:
    def __init__(self):
        self.db = Database()
        # Temporary admin credentials - should be in database
        self.admin_credentials = {
            'admin': 'admin123'
        }

    def authenticate(self, username, password):
        return username in self.admin_credentials and self.admin_credentials[username] == password

    def get_all_users(self):
        return self.db.execute_query("SELECT * FROM users")

    def get_user_data(self, user_id):
        return self.db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))

    def delete_user(self, user_id):
        return self.db.execute_query("DELETE FROM users WHERE id = %s", (user_id,))