from flask import Blueprint, request, jsonify

from api.config import get_logger
from api.app import db
from api.models import *

_logger = get_logger(logger_name=__name__)


prediction_app = Blueprint('prediction_app', __name__)


@prediction_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        _logger.info('health status OK')
        sc = ScoreTypes()
        sc.label = "Random Label"
        db.session.add(sc)
        db.session.commit()
        return "wtv"