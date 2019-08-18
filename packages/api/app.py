from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.config import get_logger
from api.utils import import_json

_logger = get_logger(logger_name=__name__)
db = SQLAlchemy()

from api.resources.auth import *
from api.resources.benchmarks import *

def create_app(*, config_object) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('prhq_api')
    flask_app.config.from_object(config_object)
    db.init_app(flask_app)
    jwt = JWTManager(flask_app)

    # import blueprints
    # from api.controller import prhq_app
    # flask_app.register_blueprint(prhq_app)
    _logger.debug('Application instance created')
    
    import api.models

    with flask_app.app_context():

        db.create_all()
        create_initial_values()

    configure_resources(flask_app)

    return flask_app


def configure_resources(app):

    rest_api = Api(app)

    rest_api.add_resource(UserRegistration, '/registration')
    rest_api.add_resource(UserLogin, '/login')
    rest_api.add_resource(UserLogoutAccess, '/logout/access')
    rest_api.add_resource(UserLogoutRefresh, '/logout/refresh')
    rest_api.add_resource(TokenRefresh, '/token/refresh')
    rest_api.add_resource(AllUsers, '/users')
    rest_api.add_resource(SecretResource, '/secret')
    rest_api.add_resource(AllGirlsResouce, '/girls')

def create_initial_values(*args, **kwargs):

    from api.initial_data import data
    
    data.load_initial_data(db)
