from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import User,CreditRequest,Document
from utils import db
from datetime import datetime, timezone
from functools import wraps

adminBP = Blueprint('adminBP', __name__)

def adminRequired(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decoratedFunction


@adminBP.route('/dashboard', methods=['GET'])
@login_required
@adminRequired
def adminDashboard():
    pendingRequests = CreditRequest.query.filter_by(status='pending').all()
    users = User.query.filter(User.is_admin == False).all()
    return jsonify({
        'pending_requests': [{
            'id': req.id,
            'user_id': req.user_id,
            'amount': req.amount,
            'created_at': req.created_at.isoformat()
        } for req in pendingRequests],
        'users': [{
            'id': user.id,
            'username': user.username,
            'credits': user.credits,
            'document_count': user.documents.count()
        } for user in users],
        'total_documents': Document.query.count()
    }), 200