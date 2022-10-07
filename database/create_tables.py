import sqlite3 

connection_obj = sqlite3.connect('test.db')

cursor_obj = connection_obj.cursor() 

cursor_obj.execute("DROP TABLE IF EXISTS vehicle;")
cursor_obj.execute("DROP TABLE IF EXISTS owner;")
cursor_obj.execute("DROP TABLE IF EXISTS owned_vehicle;")
cursor_obj.execute("DROP TABLE IF EXISTS recall;")


create_vehicle_table = """CREATE TABLE vehicle  ( 
                    vehicle_id INT PRIMARY KEY,
                    make CHAR(25) NOT NULL,
                    model CHAR(25) NOT NULL, 
                    year INT NOT NULL, 
                    windshield_wiper_front_size TEXT, 
                    windshield_wiper_rear_size TEXT, 
                    engine_oil_viscosity TEXT, 
                    engine_oil_capacity REAL, 
                    tire_pressure INT); """

create_owner_table = """CREATE TABLE owner  ( 
                    owner_id INT PRIMARY KEY,
                    first_name CHAR(25) NOT NULL,
                    last_name CHAR(25) NOT NULL, 
                    full_name CHAR(50) NOT NULL); """

create_owned_vehicle_table = """CREATE TABLE owned_vehicle  ( 
                    owned_vehicle_id INT PRIMARY KEY,
                    vehicle_id INT NOT NULL,
                    owner_id INT NOT NULL, 
                    make CHAR(25) NOT NULL,
                    model CHAR(25) NOT NULL, 
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
                    last_maintenance_appointment datetime); """

create_recall_table = """CREATE TABLE recall  ( 
                    recall_id INT PRIMARY KEY,
                    vehicle_id INT NOT NULL, 
                    description TEXT,
                    recommended_action TEXT, 
                    consequence TEXT, 
                    recall_date datetime, 
                    recall_number TEXT,  
                    campaign_number TEXT); """


create_table_queries = [create_vehicle_table, create_owner_table, create_owned_vehicle_table, create_recall_table]

for create_statement in create_table_queries: 
    cursor_obj.execute(create_statement)

print("Vehicle, owner, owned_vehicle, and recall tables are ready") 

connection_obj.close() 

