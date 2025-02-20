from flask import Blueprint, jsonify, request
from models import User,CreditRequest,Document
from utils import token_required
from utils import db
from datetime import datetime, timezone
from functools import wraps

adminBP = Blueprint('adminBP', __name__)

def adminRequired(f):
    @wraps(f)
    def decoratedFunction(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    return decoratedFunction


@adminBP.route('/dashboard', methods=['GET'])
@token_required
@adminRequired
def adminDashboard(current_user):
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@adminBP.route('/credit-requests/<int:request_id>', methods=['PUT'])
@token_required
@adminRequired
def handleCreditRequest(current_user,request_id):
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action not in ['approve', 'reject']:
            return jsonify({'error': 'Invalid action'}), 400
        
        creditRequest = CreditRequest.query.get_or_404(request_id)
        current_time = datetime.now(timezone.utc)
        
        if action == 'approve':
            creditRequest.status = 'approved'
            creditRequest.processed_at = current_time
            creditRequest.processed_by = current_user.id
            user = User.query.get(creditRequest.user_id)
            user.credits += creditRequest.amount
        else:
            creditRequest.status = 'rejected'
            creditRequest.processed_at = current_time
            creditRequest.processed_by = current_user.id
        
        db.session.commit()
        
        return jsonify({
            'message': f'Credit request {action}d',
            'request': {
                'id': creditRequest.id,
                'status': creditRequest.status,
                'processed_at': creditRequest.processed_at.isoformat()
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@adminBP.route('/analytics', methods=['GET'])
@token_required
@adminRequired
def analytics(current_user):
    user_stats = db.session.query(
        User.username,
        db.func.count(Document.id).label('scan_count')
    ).join(Document).group_by(User.id).all()
    
    credit_stats = db.session.query(
        User.username,
        User.credits
    ).filter(User.is_admin == False).all() 
    
    doc_stats = db.session.query(
        db.func.substr(Document.title, -4).label('extension'),
        db.func.count().label('count')
    ).group_by('extension').all()
    
    return jsonify({
        'user_statistics': [{
            'username': stat[0],
            'scan_count': stat[1]
        } for stat in user_stats],
        'credit_statistics': [{
            'username': stat[0],
            'credits': stat[1]
        } for stat in credit_stats],
        'document_statistics': [{
            'extension': stat[0],
            'count': stat[1]
        } for stat in doc_stats]
    }), 200