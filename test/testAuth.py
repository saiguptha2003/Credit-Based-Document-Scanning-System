import json
import pytest
import create_app
from models import User
from utils import db

@pytest.fixture
def client():
    app = create_app('testing')  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client
        db.drop_all() 

def testRegisterSuccess(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    assert b'Registration successful' in response.data

def testRegisterMissingFields(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com'
       
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

def testRegisterUsernameExists(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'new@example.com',
        'password': 'anotherpassword'
    })
    assert response.status_code == 400
    assert b'Username already exists' in response.data

def testRegisterEmailExists(client):
    client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'test@example.com',
        'password': 'anotherpassword'
    })
    assert response.status_code == 400
    assert b'Email already registered' in response.data