from api.app import create_app
from api.config import DevelopmentConfig, ProductionConfig


application = create_app(
    config_object=ProductionConfig)

@application.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(ProductionConfig.DB_URL):
        print('Deleting database.')
        drop_database(ProductionConfig.DB_URL)
    if not database_exists(ProductionConfig.DB_URL):
        print('Creating database.')
        create_database(ProductionConfig.DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny!')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
