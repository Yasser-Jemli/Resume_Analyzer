from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config.settings import Settings
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(Settings)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')  # Add this line
    Settings.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Register blueprints
        from .views.admin_view import admin_view
        from .controllers.resume_controller import resume_bp
        from .controllers.user_controller import user_bp
        
        app.register_blueprint(admin_view, url_prefix='/admin')
        app.register_blueprint(resume_bp, url_prefix='/resume')
        app.register_blueprint(user_bp, url_prefix='/user')
        
        # Add default route
        @app.route('/')
        def index():
            return redirect(url_for('admin.admin_login'))
    
    return app