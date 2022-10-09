"""
Configuration options
"""
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    FLASK_APP = 'wsgi.py'
    path = os.path.abspath(os.getcwd())
    db_uri = f'sqlite:////{path}/database.db'
    SECRET_KEY = 'testing'


class DevelopmentConfig(BaseConfig):
    TESTING = True
    DEBUG = True
