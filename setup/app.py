from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
from utils import createAdminUser, init_db
from flask_login import LoginManager
from routes import authBP, scanBP, adminBP
login_manager = LoginManager()

def createApp():
    app = Flask(__name__)
    
    app.config.update(
        SQLALCHEMY_DATABASE_URI='sqlite:///document_scanner.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'your-secret-key-here'),
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        UPLOAD_FOLDER='uploads',
        DAILY_FREE_CREDITS=20
    )
    init_db(app)
    CORS(app)
    login_manager.init_app(app)
    app.register_blueprint(authBP,url_prefix='/api/auth')
    app.register_blueprint(scanBP,url_prefix='/api/scan')
    app.register_blueprint(adminBP,url_prefix='/api/admin')
    with app.app_context():
        createAdminUser()
    return app