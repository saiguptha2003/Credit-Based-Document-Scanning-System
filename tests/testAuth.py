import sys
import os
import warnings
from setup.app import createApp
import pytest
from utils import db

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def client():
    app = createApp()  
    with app.test_client() as client:
        with app.app_context():
            db.create_all() 
        yield client
        db.drop_all()



def testRegisterSuccess(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    assert b'Registration successful' in response.data

def testRegisterMissingFields(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

def testRegisterUsernameExists(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'new@example.com',
        'password': 'anotherpassword'
    })
    assert response.status_code == 400
    assert b'Username already exists' in response.data

def testRegisterEmailExists(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'anotherpassword'
    })
    assert response.status_code == 400
    assert b'Email already registered' in response.data

def testLoginSuccess(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'securepassword'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

def testLoginMissingFields(client):
    response = client.post('/api/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

def testLoginInvalidCredentials(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid credentials' in response.data

def testLoginNonExistentUser(client):
    response = client.post('/api/auth/login', json={
        'username': 'nonexistentuser',
        'password': 'somepassword'
    })
    assert response.status_code == 404
    assert b'User not found' in response.data
