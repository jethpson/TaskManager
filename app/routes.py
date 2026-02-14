from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required
from . import db
from .models import User

# Blueprint for user-related routes
users_bp = Blueprint('users', __name__)

# -------------------------
# Frontend Pages
# -------------------------
@users_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@users_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


# -------------------------
# User API Endpoints
# -------------------------
@users_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'User {user.username} created successfully'}), 201


@users_bp.route('/login', methods=['POST'])
def login_user_endpoint():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': f'User {user.username} logged in successfully'})


@users_bp.route('/logout', methods=['GET'])
@login_required
def logout_user_endpoint():
    logout_user()
    return redirect(url_for('users.login_page'))


# -------------------------
# Dashboard (requires login)
# -------------------------
@users_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    return render_template('index.html')
