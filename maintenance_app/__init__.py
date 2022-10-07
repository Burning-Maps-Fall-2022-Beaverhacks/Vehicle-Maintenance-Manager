"""
Contains initialization settings for the app.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import config


# Globally accessible libraries
db = SQLAlchemy()

# Create App


def create_app(test_config=None):

    # Configuration
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('config.DevelopmentConfig')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Create app database if it does not exist already
    if not os.path.exists('databse.db'):
        try:
            conn = sqlite3.connect('database.sqlite')
            print('Database formed')
        except Exception as error:
            return error

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    return app
