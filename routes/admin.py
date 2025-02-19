from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import User,CreditRequest,Document
from utils import db
from datetime import datetime, timezone
from functools import wraps

adminBP = Blueprint('adminBP', __name__)
