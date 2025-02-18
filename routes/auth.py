from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from utils import db

authBP = Blueprint('authBP', __name__)
