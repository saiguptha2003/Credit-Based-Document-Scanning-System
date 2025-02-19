from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
from utils import init_db, db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_login import LoginManager

from models import User
from setup.app import createApp

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


if __name__ == '__main__':
    app = createApp()
    setupScheduler(app)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)