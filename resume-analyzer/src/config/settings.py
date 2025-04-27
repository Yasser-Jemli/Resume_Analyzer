# settings.py

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://appuser:yourpassword@localhost/sra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Debug settings
    DEBUG = True
    
    @staticmethod
    def init_app(app):
        os.makedirs(Settings.UPLOAD_FOLDER, exist_ok=True)