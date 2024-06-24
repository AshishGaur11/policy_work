from flask import render_template, redirect, url_for, flash, request
from app.auth.models import User
from app import db, login_manager  # Import login_manager
from flask_login import login_user, logout_user, current_user, login_required  # Import login-related functions and decorators
from app.auth import auth_bp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If the user is already logged in, redirect them to the index page
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)  # Log the user in using login_user()
            flash('You have been logged in.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # If the user is already logged in, redirect them to the index page
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required  # This decorator ensures that the user is logged in before accessing the route
def logout():
    logout_user()  # Log the user out using logout_user()
    flash('You have been logged out.','success')
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.", 'danger')
    return redirect(url_for('auth.login'))  