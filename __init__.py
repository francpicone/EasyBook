import os
import mysql.connector
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert, create_engine


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'SuperSecretKey'
    #  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass123@localhost:3306/EasyBook'
    #  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #  app.config['SQLALCHEMY_ECHOSQLALCHEMY_ECHO'] = True
    #  db = SQLAlchemy(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import db
    db.initialize_db()

    return app
