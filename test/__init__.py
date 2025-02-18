import json
import pytest
from app import create_app
from models import User
from utils import db

@pytest.fixture
def client():
    app = create_app('testing')  # Ensure you have a testing configuration
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database tables
        yield client
        db.drop_all()  # Clean up after tests

def test_register_success(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    assert b'Registration successful' in response.data

def test_register_missing_fields(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com'
        # Missing password
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

def test_register_username_exists(client):
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

def test_register_email_exists(client):
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