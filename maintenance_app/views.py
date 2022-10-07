"""
A view function is the code you write to respond to requests.
Flask uses patterns to match the incoming request URL to the view that should handle it.
"""
from flask import current_app as app
# A simple page that says hello


@app.route('/hello')
def hello():
    return '<h1>Hello, world!</h1>'
