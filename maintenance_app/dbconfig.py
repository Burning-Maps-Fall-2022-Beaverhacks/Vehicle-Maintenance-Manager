"""
Contains functions that initalize the app's database tables.
"""

from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, DateTime
from config import BaseConfig

database_uri = BaseConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(database_uri, echo=True)

"""
This area will contain queries to initialize the database tables.
"""
