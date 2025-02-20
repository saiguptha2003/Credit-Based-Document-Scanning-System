from flask import Blueprint, jsonify, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from utils import db
from werkzeug.security import check_password_hash
import jwt
import datetime
from utils import token_required
import logging

authBP = Blueprint('authBP', __name__)

JWT_SECRET_KEY = 'your-secret-key'  # Move this to environment variables in production
JWT_ALGORITHM = 'HS256'
@authBP.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(username=data['username'], email=data['email'])
        user.setPassword(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@authBP.route('/login', methods=['POST'])
def login():    
    try:
        data = request.get_json()
        if not data:
            logging.error("No JSON data received in login request")
            return jsonify({'error': 'No data provided'}), 400
            
        logging.info(f"Login attempt for username: {data.get('username', 'not provided')}")
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.checkPassword(data.get('password')):
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            }, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'credits': user.credits,
                    'is_admin': user.is_admin
                }
            }), 200
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@authBP.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return jsonify({'message': 'Logout successful'}), 200

@authBP.route('/verify-token', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({
        'message': 'Valid token',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email
        }
    }), 200