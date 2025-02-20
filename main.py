from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
from utils import init_db, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from models import User
from setup.app import createApp

logging.basicConfig(level=logging.DEBUG)
def setupScheduler(app):
    scheduler = BackgroundScheduler()
    def resetDailyCredits():
        with app.app_context():
            users = User.query.all()
            for user in users:
                user.credits = app.config['DAILY_FREE_CREDITS']
            db.session.commit()
    scheduler.add_job(
        func=resetDailyCredits,
        trigger=CronTrigger(hour=0, minute=0),
        id='reset_credits',
        name='Reset daily credits at midnight',
        replace_existing=True
    )
    scheduler.start()

app = createApp()
CORS(app, resources={
r"*": {
    "origins": "http://127.0.0.1:5500",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "supports_credentials": True
}
})
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

if __name__ == '__main__':
    setupScheduler(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
