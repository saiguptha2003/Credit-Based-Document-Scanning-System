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

