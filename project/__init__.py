import os

from flask import Flask

from . import config
from .auth import login_manager
from .models import db, migrate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    # use instance path for test db (default in flask_sqlalchemy 3.0.0)
    if '{instance_path}' in app.config['SQLALCHEMY_DATABASE_URI']:
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            app.config['SQLALCHEMY_DATABASE_URI'].format(
                instance_path=app.instance_path)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from . import auth, course, home
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(auth.google_bp, url_prefix='/auth')
    app.register_blueprint(auth.github_bp, url_prefix='/auth')
    app.register_blueprint(course.bp, url_prefix='/course/<course_code>')

    return app
