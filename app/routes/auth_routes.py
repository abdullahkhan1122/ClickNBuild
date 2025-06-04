from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, Client, Builder
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('auth/signup_form.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role-login')

    if not email or not password or not role:
        # flash('All fields are required.', 'danger')
        return redirect(url_for('auth.signup'))

    sql = text("SELECT user_id, username, email, password, phone, role FROM USER WHERE email = :email LIMIT 1")
    result = db.session.execute(sql, {'email': email}).fetchone()

    if result:
        user_password = result.password

        if check_password_hash(user_password, password):
            # Save login session
            session['user_email'] = result.email
            session['user_id'] = result.user_id
            session['role'] = result.role

            # flash('Logged in successfully!', 'success')

            # Route based on role
            if result.role == 'Client':
                return redirect(url_for('client.clientHomepage'))
            elif result.role == 'Builder':
                return redirect(url_for('builder.builder_homepage'))
            else:
                # flash('Invalid role detected.', 'danger')
                return redirect(url_for('auth.signup'))
        else:
            # flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.signup'))
    else:
        # flash('Invalid email or password.', 'danger')
        return redirect(url_for('auth.signup'))


@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    role = request.form.get('role-register')  

    if not (username and email and password and role):
        # flash('All fields are required.', 'danger')
        return redirect(url_for('auth.signup'))

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        # flash('Email already registered. Please login or use a different email.', 'danger')
        return redirect(url_for('auth.signup'))

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        role=role,
        phone=phone
    )

    db.session.add(new_user)
    db.session.commit()

    # Create Client or Builder
    if role == 'Client':
        new_client = Client(user_id=new_user.user_id)
        db.session.add(new_client)
        db.session.commit()

    elif role == 'Builder':
        new_builder = Builder(
            user_id=new_user.user_id,
            active_bids=0,
            rating=0.0,
            total_projects=0,
            total_earning=0
        )
        db.session.add(new_builder)
        db.session.commit()

    # flash('Registration successful! Please login.', 'success')
    return redirect(url_for('auth.signup'))



# Logout 

@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Destroys all session info
    return redirect(url_for('client.websiteHomepage'))  # if defined in client_routes.py
