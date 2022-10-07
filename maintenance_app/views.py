"""
A view function is the code you write to respond to requests.
Flask uses patterns to match the incoming request URL to the view that should handle it.
"""
from flask import current_app as app
import requests


# A simple page that says hello


@app.route('/hello')
def hello():
    return '<h1>Hello, world!</h1>'


# API Testing
header = {
    "content-type": "application/json",
    "authorization": "Basic NjA1NjRlNjEtY2Y4Mi00YjNlLTk3YmUtM2Y5M2VmZjcwNmEz",
    "partner-token": "0ce7897ec7654f44bc40115fafef29c0"
}


@app.route('/api-test')
def api_test():
    vin = requests.get(
        'http://api.carmd.com/v3.0/decode?vin=1GNALDEK9FZ108495', headers=header)
    return f'{vin.json()}'
