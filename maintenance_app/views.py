"""
A view function is the code you write to respond to requests.
Flask uses patterns to match the incoming request URL to the view that should handle it.
"""

from flask import current_app as app
import requests
import json


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
    # vin_request = requests.get(
    #     'http://api.carmd.com/v3.0/decode?vin=1GNALDEK9FZ108495', headers=header)
    # request_json = vin_request.json()
    request_json = {
        "message": {
            "code": 0,
            "message": "ok",
            "credentials": "valid",
            "version": "v3.0.0",
            "endpoint": "decode",
            "counter": 5
        },
        "data": {
            "year": 2015,
            "make": "CHEVROLET",
            "model": "EQUINOX",
            "manufacturer": "GENERAL MOTORS",
            "engine": "L4, 2.4L; DOHC; 16V; DI; FFV",
            "trim": "LTZ",
            "transmission": "AUTOMATIC"
        }
    }
    vin = '1GNALDEK9FZ108495'
    make = request_json['data']['make']
    model = request_json['data']['model']
    manufacturer = request_json['data']['manufacturer']
    transmission = request_json['data']['transmission']
    year = request_json['data']['year']
    engine = request_json['data']['engine']
    trim = request_json['data']['trim']
    return f'VIN: {vin}, Make: {make}, Model: {model}, Manufacturer: {manufacturer},\
        Transmission: {transmission}, Year: {year}, Engine: {engine}, Trim: {trim}'
