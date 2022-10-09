import sqlite3 

connection_obj = sqlite3.connect('database.sqlite')

cursor_obj = connection_obj.cursor() 

# mock data                
owner_records = [("James", "McGill", "James McGill"),
                 (2, "Kim", "Wexler", "Kim Wexler"), 
                 (3, "Michael", "Scott", "Michael Scott")]


cursor_obj.executemany('INSERT INTO owner values (?,?, ?, ?)', owner_records)
connection_obj.commit()
print(f'{cursor_obj.rowcount} records were inserted into the owner table')


connection_obj.close() 
