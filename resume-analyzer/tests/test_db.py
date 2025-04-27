from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.settings import Settings

def test_connection():
    app = Flask(__name__)
    app.config.from_object(Settings)
    db = SQLAlchemy(app)
    
    try:
        with app.app_context():
            db.engine.connect()
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()