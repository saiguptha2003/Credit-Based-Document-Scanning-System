import sys
import os
import warnings
from setup.app import createApp, login_manager
import pytest
from utils import db
from flask_login import login_user
from models import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def app():
    app = createApp()
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def admin_user(app, client):
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.setPassword('securepassword')
            db.session.add(admin)
            db.session.commit()
        return admin

def testAdminDashboardSuccess(app, client, admin_user):
    with client.session_transaction() as session:
        session['_user_id'] = admin_user.id
        session['_fresh'] = True
    
    response = client.get('/api/admin/dashboard')
    assert response.status_code == 200
    assert b'pending_requests' in response.data
    assert b'users' in response.data
    assert b'total_documents' in response.data

def testAdminDashboardAccessDenied(app, client):
    response = client.get('/api/admin/dashboard')
    assert response.status_code == 401
    assert b'Unauthorized' in response.data

def testAdminDashboardNonAdminAccess(app, client):
    non_admin_id = None
    with app.app_context():
        non_admin = User.query.filter_by(username='user').first()
        if not non_admin:
            non_admin = User(username='user', email='user@example.com', is_admin=False)
            non_admin.setPassword('securepassword')
            db.session.add(non_admin)
            db.session.commit()
        non_admin_id = non_admin.id
    
    with client.session_transaction() as session:
        session['_user_id'] = non_admin_id
        session['_fresh'] = True
    
    response = client.get('/api/admin/dashboard')
    assert response.status_code == 403
    assert b'Admin access required' in response.data
