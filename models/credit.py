from utils import db
from datetime import datetime, timezone

class CreditRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')  
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc).isoformat())
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Define relationships with explicit foreign keys
    requester = db.relationship('User', foreign_keys=[user_id], backref='credit_requests')
    processor = db.relationship('User', foreign_keys=[processed_by], backref='processed_requests')