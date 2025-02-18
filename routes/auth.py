from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from utils import db

authBP = Blueprint('authBP', __name__)


@authBP.route('/register', methods=['POST'])
def register():
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