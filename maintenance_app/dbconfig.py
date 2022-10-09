"""
Contains queries to initialize the database tables.
"""


def create_tables(connection_obj):
    """
    Create database tables
    """

    cursor_obj = connection_obj.cursor()

    cursor_obj.execute("DROP TABLE IF EXISTS vehicle;")
    cursor_obj.execute("DROP TABLE IF EXISTS owner;")
    cursor_obj.execute("DROP TABLE IF EXISTS owned_vehicle;")
    cursor_obj.execute("DROP TABLE IF EXISTS recall;")
    cursor_obj.execute("DROP TABLE IF EXISTS service_master;")

    create_vehicle_table = """CREATE TABLE vehicle  ( 
                        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        make CHAR(25) NOT NULL,
                        model CHAR(25) NOT NULL, 
                        year INT NOT NULL, 
                        windshield_wiper_front_size TEXT, 
                        windshield_wiper_rear_size TEXT, 
                        engine_oil_viscosity TEXT, 
                        engine_oil_capacity REAL, 
                        vehicle_color TEXT); """

    create_owner_table = """CREATE TABLE owner  ( 
                        owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name CHAR(25) NOT NULL,
                        last_name CHAR(25) NOT NULL, 
                        full_name CHAR(50) NOT NULL, 
                        email TEXT NOT NULL, 
                        password NOT NULL); """

    create_owned_vehicle_table = """CREATE TABLE owned_vehicle  ( 
                        owned_vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vin TEXT,  
                        vehicle_id INT NOT NULL,
                        owner_id INT NOT NULL, 
                        make CHAR(25) NOT NULL,
                        model CHAR(25) NOT NULL, 
                        manufacturer TEXT NOT NULL, 
                        transmission TEXT, 
                        engine TEXT, 
                        trim TEXT, 
                        year INT NOT NULL, 
                        windshield_wiper TEXT, 
                        engine_oil TEXT, 
                        tire_pressure INT, 
                        vehicle_name TEXT, 
                        owner_first_name CHAR(25) NOT NULL,
                        owner_last_name CHAR(25) NOT NULL, 
                        owner_full_name CHAR(50) NOT NULL, 
                        mileage INT, 
                        last_oil_change datetime, 
                        last_maintenance_appointment datetime, 
                        api_call INT); """

    create_recall_table = """CREATE TABLE recall  ( 
                        recall_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vehicle_id INT, 
                        description TEXT,
                        recommended_action TEXT, 
                        consequence TEXT, 
                        recall_date datetime, 
                        recall_number TEXT,  
                        campaign_number TEXT); """

    create_maintenance_table = """CREATE TABLE maintenance  ( 
                    maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owned_vehicle_id INT, 
                    maintenance_description TEXT,
                    due_mileage INT, 
                    parts_needed TEXT, 
                    parts_price REAL, 
                    part_quantity INT, 
                    repair_difficulty INT, 
                    repair_hours REAL, 
                    repair_total_cost REAL, 
                    maintenance_date datetime, 
                    status TEXT); """



    create_table_queries = [create_vehicle_table, create_owner_table,
                            create_owned_vehicle_table, create_recall_table, 
                            create_maintenance_table]

    for create_statement in create_table_queries:
        cursor_obj.execute(create_statement)

    print("Vehicle, owner, owned_vehicle, recall, and maintenance tables are ready")

    connection_obj.close()
