import sqlite3 

connection_obj = sqlite3.connect('test.db')

cursor_obj = connection_obj.cursor() 

cursor_obj.execute('DELETE FROM vehicle;')
print(f'{cursor_obj.rowcount} records were deleted from the vehicle table')
cursor_obj.execute('DELETE FROM owner;')
print(f'{cursor_obj.rowcount} records were deleted from the owner table')

connection_obj.commit()

# mock data
vehicle_records =   [(1,'Ford', 'Fusion', 2016, '26"/26"', "", "SAE 5W-30",5.7,33),
                    (2, 'Jeep', 'Wrangler', 2020,'16"/16"', "", "SAE 5W-25",6,29),
                    (3, 'Tesla', 'Model 3', 2022,'28"/18"', "", "",None, 33)]
                
owner_records = [(1, "James", "McGill", "James McGill"),
                 (2, "Kim", "Wexler", "Kim Wexler"), 
                 (3, "Michael", "Scott", "Michael Scott")]




cursor_obj.executemany('INSERT INTO vehicle values (?,?,?,?,?,?,?,?,?)', vehicle_records)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the vehicle table')

cursor_obj.executemany('INSERT INTO owner values (?,?, ?, ?)', owner_records)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the owner table')


vehicle_select_query = """SELECT * FROM vehicle;"""
vehicle_select_result = cursor_obj.execute(vehicle_select_query)
records = cursor_obj.fetchall() 
print("Vehicle table: \n")
for row in records: 
    print([i for i in row])

owner_select_query = """SELECT * FROM owner;"""
owner_select_result = cursor_obj.execute(owner_select_query)
records = cursor_obj.fetchall() 
print("Owner table: \n")
for row in records: 
    print([i for i in row])

connection_obj.close() 
