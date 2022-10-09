"""
A view function is the code you write to respond to requests.
Flask uses patterns to match the incoming request URL to the view that should handle it.
"""

from flask import current_app as app, request, render_template, redirect, url_for
import requests
import json
import sqlite3
from . import apiconfig, forms
import database.api_response_tests
import pprint


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
    vehicle_id = request.args.get("vehicle")
    owned_vehicle_id = request.args.get("owned_vehicle")

    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    has_api_been_called = cursor_obj.execute(
        'SELECT api_call FROM owned_vehicle WHERE owned_vehicle_id = ?', (owned_vehicle_id,)).fetchone()[0]

    # Set vehicle details
    car_info = cursor_obj.execute(
        'SELECT year, make, model, mileage FROM owned_vehicle WHERE owned_vehicle_id = ?;', (owned_vehicle_id,)).fetchone()
    year = car_info[0]
    make = car_info[1]
    model = car_info[2]
    miles_driven = car_info[3]

    if has_api_been_called != 1:
        # make api call for maintenance and recall
        api_get_maintenance_test(
            year, make, model, miles_driven, owned_vehicle_id)
        api_get_recall_test(year, make, model)
        cursor_obj.execute(
            'UPDATE owned_vehicle SET api_call = 1 WHERE owned_vehicle_id =?', (owned_vehicle_id,))
        connection_obj.commit()

    # maintenance info
    complete_status = 'Complete'
    maintenance = cursor_obj.execute(
        'SELECT maintenance_id, maintenance_description, repair_difficulty, due_mileage, status FROM maintenance WHERE owned_vehicle_id = ? AND status != ?;', (owned_vehicle_id, complete_status)).fetchmany(6)
    col_names = ["maintenance_id", "service", "difficulty", "mileage", "status"]
    maintenance_list = []
    for row in maintenance:
        if row[-1] != 'Complete': 
            maintenance_dict = {}
            for i, col in enumerate(col_names):
                maintenance_dict[col] = row[i]
            maintenance_list.append(maintenance_dict)
    print("Maintenance list: ", maintenance,
          "\n Owned Vehicle ID: ", owned_vehicle_id)

    # recall info
    recall = cursor_obj.execute(
        'SELECT recall_number, description, recommended_action, consequence, recall_date FROM recall WHERE vehicle_id = ? ORDER BY recall_date DESC;', (vehicle_id,)).fetchmany(5)
    recall_col_names = ["recall_number",
                        "description", "action", "consequence", "date"]
    recall_list = []
    for row in recall:
        recall_dict = {}
        for i, col in enumerate(recall_col_names):
            if col not in ("recall_number", "date"):
                recall_dict[col] = row[i].capitalize()
            else:
                recall_dict[col] = row[i]
        recall_list.append(recall_dict)

    print(recall_list)

    return render_template(
        'view-vehicle.html',
        year=year,
        make=make,
        model=model,
        maint=maintenance_list[:5],
        recalls=recall_list,
        vehicle_id=vehicle_id,
        owned_vehicle_id=owned_vehicle_id,
    )


@app.route('/service')
def service():
    vehicle_id = request.args.get("vehicle")
    owned_vehicle_id = request.args.get("owned_vehicle")
    maintenance_id = request.args.get("maintenance_id")
    status = request.args.get("status")

    if status == "Complete":
        # return f"<h1>{status}</h1>"
        # Query db; change status to complete
        connection_obj = sqlite3.connect('database.sqlite')
        cursor_obj = connection_obj.cursor()    
        cursor_obj.execute(
            'UPDATE maintenance SET status = ? WHERE maintenance_id = ?;', (status, maintenance_id,)) 
        connection_obj.commit()
        connection_obj.close()

    return redirect(f'/view?vehicle_id={vehicle_id}&owned_vehicle={owned_vehicle_id}')


@app.route('/dashboard/<int:owner_id>', methods=["GET", "POST"])
def dashboard(owner_id):
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()
    dashboard_columns = ["year", "make", "model",
                         "owner_id", "vehicle_id", "owned_vehicle_id"]
    dashboard_vehicle = cursor_obj.execute(
        'SELECT year, make, model, owner_id, vehicle_id, owned_vehicle_id FROM owned_vehicle;').fetchall()
    vehicle_list = []
    for row in dashboard_vehicle:
        vehicle_dict = {}
        for i, col in enumerate(dashboard_columns):
            vehicle_dict[col] = row[i]
        vehicle_list.append(vehicle_dict)

    # Add Vehicle form handling
    form = forms.AddVehicleForm(request.form)
    print(form)
    if form.validate_on_submit():
        return redirect("dashboard")
    
    if request.method == "POST":
        year = request.form.get("year")
        make = request.form.get("make")
        model = request.form.get("model")
        mileage = request.form.get("mileage")
        color = request.form.get("color")
        # return f"<h1>You did it, {name}!</h1>"
        connection_obj = sqlite3.connect('database.sqlite')
        cursor_obj = connection_obj.cursor()

        # insert into vehicle table
        vehicle_record = (None, make, model, year, "", "", "", "", color)
        cursor_obj.execute(
            'INSERT INTO vehicle values (?,?,?,?,?,?,?,?,?)', vehicle_record)
        connection_obj.commit()
    
        vehicle_id = cursor_obj.execute(
            'SELECT MAX(vehicle_id) FROM vehicle;').fetchone()[0]

        owner_info = cursor_obj.execute('SELECT first_name, last_name, full_name FROM owner WHERE owner_id = ?', (owner_id,)).fetchone()
        connection_obj.commit()
        owned_vehicle = (None, "", vehicle_id, owner_id, make, model, "", "", "", "", year, "", "", "", "", owner_info[0], owner_info[1], owner_info[2], mileage, "", "", 0)

        cursor_obj.execute(
            'INSERT INTO owned_vehicle values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', owned_vehicle)
        connection_obj.commit()
        connection_obj.close()


    return render_template(
        'dashboard.html',
        vehicles=vehicle_list,
        form=form
    )


@ app.route('/api-test')
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


# @ app.route('/api-get-maintenance')
def api_get_maintenance_test(year, make, model, miles_driven, owned_vehicle_id):

    make = make.upper()
    model = model.upper()

    maintenance_request = requests.get(
        f"http://api.carmd.com/v3.0/maint?year={year}&make={make}&model={model}&mileage={miles_driven}", headers=apiconfig.header)
    maintenance_json = maintenance_request.json()

    # create connection to database
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    # iterate through JSON and send to table in database

    # for maintenance_item in database.api_response_tests.maintenance_example_one['data']:
    for maintenance_item in maintenance_json['data']:
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

        insert_data = (None, owned_vehicle_id, maintenance_item['desc'], maintenance_item['due_mileage'], part_needed,
                       part_price, part_quantity, repair_difficulty, repair_hours, repair_total_cost, None, "Incomplete")
        print(insert_data)
        cursor_obj.execute(
            'INSERT INTO maintenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', insert_data)
        connection_obj.commit()

    connection_obj.close()


# @ app.route('/api-get-recall')
def api_get_recall_test(year, make, model):
    make = make.upper()
    model = model.upper()
    recall_request = requests.get(
        f"http://api.carmd.com/v3.0/recall?year={year}&make={make}&model={model}", headers=apiconfig.header)
    recall_json = recall_request.json()

    # create connection to database
    connection_obj = sqlite3.connect('database.sqlite')
    cursor_obj = connection_obj.cursor()

    # iterate through JSON and send to table in database
    for recall in recall_json['data']:
        # for recall in database.api_response_tests.recall_example_three['data']:
        insert_data = (None, 1, recall['desc'], recall['corrective_action'], recall['consequence'],
                       recall['recall_date'], recall['recall_number'], recall['campaign_number'])
        cursor_obj.execute(
            'INSERT INTO recall VALUES (?,?,?,?,?,?,?,?)', insert_data)
        connection_obj.commit()

    connection_obj.close()

    return f'It worked'
