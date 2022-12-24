from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import config

app = Flask(__name__,template_folder="build",static_folder="build/static")
app.config.from_object(config)
db = SQLAlchemy()
# login_manager = LoginManager()
db.init_app(app)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def register_blueprints():
    from app.home import home,views
    from app.api import api,views

    blueprints = [home,api]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

register_blueprints()
configure_database(app)
