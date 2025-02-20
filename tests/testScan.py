import io
import sys
import os
import warnings
from setup.app import createApp
import pytest
from utils import db
from flask_login import LoginManager
from models import Document, User

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def client():
    app = createApp()
    login_manager = LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            test_user = User(
                username='testuser',
                email='test@example.com',
            )
            test_user.setPassword('securepassword')
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()
def login_test_user(client):
    return client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'securepassword'
    })

def testScanDocumentNoFile(client):
    login_test_user(client)
    response = client.post('/api/scan/scan-document', 
                         data={},
                         content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'No file provided' in response.data

def testScanDocumentInvalidFileType(client):
    login_test_user(client)
    test_file = (io.BytesIO(b"test content"), 'test.invalid')
    response = client.post('/api/scan/scan-document', 
                         data={'file': test_file},
                         content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'File type not allowed' in response.data
