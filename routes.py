# routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User
import secrets

# Create a Blueprint for organizing routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Redirect to the main page if the user is logged in, otherwise redirect to the auth page."""
    if 'username' in session:
        return redirect(url_for('main.main_page'))
    return redirect(url_for('main.auth'))

@main.route('/auth', methods=['GET', 'POST'])
def auth():
    """Handle user authentication: login and display the login form."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real application, use hashed passwords

        user = User.query.filter_by(username=username).first()
        if user:
            session['username'] = username  # Set the session variable for the logged-in user
            return redirect(url_for('main.main_page'))
        else:
            flash('Invalid username or password', 'danger')  # Flash an error message

    return render_template('auth.html')  # Render the authentication page

@main.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration: create a new user and display the registration form."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real application, hash the password

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))

        # Create a new user and add to the database
        new_user = User(username=username, wallet_address=secrets.token_hex(32))  # Generate a random wallet address
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.auth'))  # Redirect to the login page

    return render_template('register.html')  # Render the registration page

@main.route('/main')
def main_page():
    """Display the main wallet page for the logged-in user."""
    if 'username' not in session:
        return redirect(url_for('main.auth'))
    
    user = User.query.filter_by(username=session['username']).first()
    return render_template('wallet.html', user=user)

@main.route('/logout')
def logout():
    """Log the user out by removing their session and redirect to the auth page."""
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('main.auth'))  # Redirect to the authentication page
