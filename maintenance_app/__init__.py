"""
Contains initialization settings for the app.
"""
import os
from flask import Flask
import sqlite3
from . import dbconfig
import config


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
    if not os.path.exists('database.sqlite'):
        try:
            connection_obj = sqlite3.connect('database.sqlite')
            dbconfig.create_tables(connection_obj)
            print('Database formed')

        except Exception as error:
            return error

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        # Include routes
        from . import views

    return app
