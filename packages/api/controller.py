from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user

from api.config import get_logger
from api.app import db, login_manaager
from api.models import *

_logger = get_logger(logger_name=__name__)

prhq_app = Blueprint('prediction_app', __name__)

@prhq_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        _logger.info('health status OK')
        sc = ScoreTypes()
        sc.label = "Random Label"
        db.session.add(sc)
        db.session.commit()
        return "wtv"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "user is already authenticated"
    
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        return "WRONG"
    
    login_user(user)
    return "COOL"!

@app.route('/logout')
def logout():
    logout_user()
    return "out"

@login.user_loader
def load_user(id):
    return User.query.get(int(id))