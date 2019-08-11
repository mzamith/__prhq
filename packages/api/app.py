from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from api.config import get_logger


_logger = get_logger(logger_name=__name__)
db = SQLAlchemy()


def create_app(*, config_object) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('prhq_api')
    flask_app.config.from_object(config_object)
    db.init_app(flask_app)

    # import blueprints
    from api.controller import prediction_app
    flask_app.register_blueprint(prediction_app)
    _logger.debug('Application instance created')
    
    import api.models

    with flask_app.app_context():

        db.create_all()

    return flask_app
