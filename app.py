"""
ECOTECH SERVICES - Flask Web Application
Main application entry point with Flask app factory pattern
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime

# Import extensions
from extensions import db, login_manager, migrate, csrf

def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__)
    
    # Configuration
       
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ecotech-dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://u483781610_somilpandey:Somil1234%23@srv1495.hstgr.io:3306/u483781610_ecotechh'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access the admin dashboard.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Admin
        # Replace Admin.query.get() with db.session.get()
        return db.session.get(Admin, int(user_id))
    
    # Import and register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables and default admin
    with app.app_context():
        db.create_all()
        create_default_admin()
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(app.static_folder, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Add a favicon route to prevent 404 errors
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')
    return app



def create_default_admin():
    """Create default admin user if none exists"""
    try:
        from models import Admin
        
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                email='admin@ecotechservices.com',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created - Username: admin, Password: admin123")
    except Exception as e:
        print(f"Error creating default admin: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables within app context
    app.run(debug=True, host='0.0.0.0', port=5000)
