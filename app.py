"""
Flask Application configured for Oracle Database
This version connects to your existing Oracle database with flight booking data
"""

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models import db, Passenger  # Use Oracle models
from datetime import datetime
import os

# Import Oracle configuration
from oracle_config import ORACLE_CONNECTION_STRING, ORACLE_ENGINE_OPTIONS, ORACLE_HOST, ORACLE_USERNAME

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = ORACLE_CONNECTION_STRING
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = ORACLE_ENGINE_OPTIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Show SQL queries for debugging

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login uses this to reload the user object from the user ID stored in the session.
    """
    return Passenger.query.get(int(user_id))

# Import and register blueprints (route modules)
from auth_routes import auth_bp
from user_routes import user_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

# Home route
@app.route('/')
def index():
    """
    Home page - redirects to search if logged in, otherwise to login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.search'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Flask Application with Oracle Database")
    print("="*60)
    print(f"📍 Connecting to: {ORACLE_HOST}")
    print(f"👤 Username: {ORACLE_USERNAME}")
    print(f"🔗 Database: course (SID)")
    print("="*60 + "\n")
    
    # Note: We don't run init_db() because your tables already exist in Oracle!
    # The Flask app will connect to your existing data
    
    # Run the application
    app.run(debug=True, port=5000)
