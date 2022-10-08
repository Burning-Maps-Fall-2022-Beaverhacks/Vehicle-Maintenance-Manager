from flask import current_app as app
import requests
import json
import sqlite3
import apiconfig
import database.api_response_tests
import pprint

print(apiconfig.header)