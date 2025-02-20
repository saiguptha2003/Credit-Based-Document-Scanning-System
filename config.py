import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '219d86a1-28c9-4991-a4e6-b3be133feab1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///documentScanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
    DAILY_FREE_CREDITS = 20
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or '219d86a1-28c9-4991-a4e6-b3be133feab1'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    
    

