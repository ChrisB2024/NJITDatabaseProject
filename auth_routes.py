from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models import db, Passenger
from datetime import datetime, date

# Create blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Route
    Creates a new passenger with authentication credentials
    """
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        date_of_birth_str = request.form.get('date_of_birth')
        nationality = request.form.get('nationality', 'USA')
        
        # Validation
        if not all([full_name, email, password, confirm_password, date_of_birth_str]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        # Parse date of birth
        try:
            dob = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
            return render_template('register.html')
        
        # Check if email already exists
        if Passenger.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html')
        
        # Create new passenger
        new_passenger = Passenger(
            full_name=full_name,
            email=email,
            date_of_birth=dob,
            nationality=nationality,
            phone=phone
        )
        new_passenger.set_password(password)
        
        # Add to database
        try:
            db.session.add(new_passenger)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {e}")
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Route
    Authenticates passengers by email and password
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')
        
        # Find passenger by email
        passenger = Passenger.query.filter_by(email=email).first()
        
        # Verify credentials
        if passenger and passenger.check_password(password):
            login_user(passenger)
            flash(f'Welcome back, {passenger.first_name}!', 'success')
            
            # Redirect to next page if specified, otherwise to search page
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('user.search'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    User Logout Route
    Ends the user session and redirects to login page.
    """
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
