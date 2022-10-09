import sqlite3
connection_obj = sqlite3.connect('database.sqlite')

cursor_obj = connection_obj.cursor()

# mock owners
owner_records = [(None, "James", "McGill", "James McGill", "james.mcgill@hotmail.com", "JMM"),
                 (None, "Kim", "Wexler", "Kim Wexler",
                  "kim.wexler@gmail.com", "law"),
                 (None, "Michael", "Scott", "Michael Scott", "michael.scott@yahoo.com", "password")]

cursor_obj.executemany(
    'INSERT INTO owner values (?,?,?,?,?,?)', owner_records)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the owner table')

# mock vehicles
vehicle_records = [(None, 'Ford', 'Focus', 2003, "", "", "", "", "Baby Blue"),
                   (None, 'Toyota', 'Prius', 2015, "", "", "", "", "Lime Green")]
cursor_obj.executemany(
    'INSERT INTO vehicle values (?,?,?,?,?,?,?,?,?)', vehicle_records)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the vehicle table')

# owned vehicle
owned_vehicle = [(None, "", 1, 3, "Ford", 'Focus', 'Ford', 'gasoline', "", "", 2003, "", "", "", "", "Michael", "Scott", "Michael Scott", 288000, "", "", 0),
                 (None, "", 3, 3, "Toyota", 'Prius', 'Toyota', 'hybrid', "", "", 2015, "", "", "", "", "Michael", "Scott", "Michael Scott", 112000, "", "", 0)]

cursor_obj.executemany(
    'INSERT INTO owned_vehicle values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', owned_vehicle)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the owned_vehicle table')
connection_obj.close()
