import os

from models import User
from utils import db

def createAdminUser():
    adminUsername = os.environ.get('ADMIN_USERNAME', 'admin')
    adminPassword = os.environ.get('ADMIN_PASSWORD', 'admin')
    adminEmail = os.environ.get('ADMIN_EMAIL', 'admin@srmap.com')
    if not User.query.filter_by(username=adminUsername).first():
        admin = User(
            username=adminUsername,
            email=adminEmail,
            is_admin=True
        )
        admin.setPassword(adminPassword)
        db.session.add(admin)
        db.session.commit()
