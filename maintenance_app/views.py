"""
A view function is the code you write to respond to requests.
Flask uses patterns to match the incoming request URL to the view that should handle it.
"""

from flask import current_app as app, request, redirect, render_template
import requests
import json
import sqlite3
from . import apiconfig
import database.api_response_tests
import pprint
from . import forms

# API Testing
# header = apiconifg.header


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="Car Maintenance Tracker",
        description="A WebApp to track the service your vehicles need."
    )


@app.route('/view')
def view():
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()
    col_names = ["service", "difficulty", "cost", "mileage"]

    # maintenance info
    maintenance = cursor_obj.execute(
        'SELECT maintenance_description, repair_difficulty, repair_total_cost, due_mileage FROM maintenance;').fetchmany(5)
    maintenance_list = []
    for row in maintenance:
        maintenance_dict = {}
        for i, col in enumerate(col_names):
            maintenance_dict[col] = row[i]
        maintenance_list.append(maintenance_dict)

    # recall info
    recall_col_names = ["recall_number",
                        "description", "action", "consequence", "date"]
    recall = cursor_obj.execute(
        'SELECT recall_number, description, recommended_action, consequence, recall_date FROM recall ORDER BY recall_date DESC;').fetchmany(5)
    recall_list = []
    for row in recall:
        recall_dict = {}
        for i, col in enumerate(recall_col_names):
            if col not in ("recall_number", "date"):
                recall_dict[col] = row[i].capitalize()
            else:
                recall_dict[col] = row[i]
        recall_list.append(recall_dict)

    return render_template(
        'view-vehicle.html',
        maint=maintenance_list,
        recalls=recall_list

    )


@app.route('/api-test')
def api_test():
    #     vin_request = requests.get(
    #         'http://api.carmd.com/v3.0/decode?vin=1GNALDEK9FZ108495', headers=header)
    #     request_json = vin_request.json()

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
    # Set variables to pass into the DB
    vin = '1GNALDEK9FZ108495'
    make = request_json['data']['make']
    model = request_json['data']['model']
    manufacturer = request_json['data']['manufacturer']
    transmission = request_json['data']['transmission']
    year = request_json['data']['year']
    engine = request_json['data']['engine']
    trim = request_json['data']['trim']

    insert_data = (None, vin, 1, 1, make, model, manufacturer, transmission,
                   engine, trim, year, "", "", 100, "", "James", "McGill",
                   "James McGill", 50000, '2022-06-01', '2022-06-01')

    # create connecdtion to db
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    # send data to database
    cursor_obj.execute('INSERT INTO owned_vehicle VALUES \
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', insert_data)
    connection_obj.commit()

    return f'VIN: {vin}, Make: {make}, Model: {model}, Manufacturer: {manufacturer},\
        Transmission: {transmission}, Year: {year}, Engine: {engine}, Trim: {trim}'


@app.route('/api-get-maintenance')
def api_get_maintenance_test():

    # maintenance_request = requests.get("http://api.carmd.com/v3.0/maint?year=2021&make=TOYOTA&model=COROLLA&mileage=8000", headers=apiconfig.header)
    # maintenance_json = maintenance_request.json()

    # create connection to database
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    # iterate through JSON and send to table in database

    for maintenance_item in database.api_response_tests.maintenance_example_one['data']:
        # get part data
        # pprint.pprint(maintenance_item)
        if maintenance_item['parts'] == None:
            part_needed = None
            part_price = None
            part_quantity = None
        else:
            part_needed = maintenance_item['parts'][0]['desc']
            part_price = maintenance_item['parts'][0]['price']
            part_quantity = maintenance_item['parts'][0]['qty']

        if maintenance_item['repair'] == None:
            repair_difficulty = None
            repair_hours = None
            repair_total_cost = None
        else:
            repair_difficulty = maintenance_item['repair']['repair_difficulty']
            repair_hours = maintenance_item['repair']['repair_hours']
            repair_total_cost = maintenance_item['repair']['total_cost']

        insert_data = (None, None, maintenance_item['desc'], maintenance_item['due_mileage'], part_needed,
                       part_price, part_quantity, repair_difficulty, repair_hours, repair_total_cost, None)
        cursor_obj.execute(
            'INSERT INTO maintenance VALUES (?,?,?,?,?,?,?,?,?,?,?)', insert_data)
        connection_obj.commit()

    connection_obj.close()

    return f'parts_needed:{part_needed}'


@app.route('/api-get-recall')
def api_get_recall_test():
    # recall_request = requests.get("http://api.carmd.com/v3.0/recall?year=2017&make=HONDA&model=ACCORD", headers=apiconfig.header)
    # recall_json = recall_request.json()

    # create connection to database
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    # iterate through JSON and send to table in database

    # for recall in recall_json['data']:
    for recall in database.api_response_tests.recall_example_three['data']:
        insert_data = (None, 1, recall['desc'], recall['corrective_action'], recall['consequence'],
                       recall['recall_date'], recall['recall_number'], recall['campaign_number'])
        cursor_obj.execute(
            'INSERT INTO recall VALUES (?,?,?,?,?,?,?,?)', insert_data)
        connection_obj.commit()

    connection_obj.close()

    return f'It worked'
