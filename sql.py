import sqlite3

## Connect to sqlite database
connection = sqlite3.connect('fintech.db')

##  Create a cursor object to insert record, create table, retrieve record
cursor = connection.cursor()

## Create a table
table_info = """
CREATE TABLE IF NOT EXISTS fintech(id INT PRIMARY KEY, transaction_id INT, amount FLOAT, status VARCHAR(25), date TEXT, description TEXT);

"""

cursor.execute(table_info)


## Insert record into the table
cursor.execute("INSERT INTO fintech VALUES (1, 1001, 250.75, 'Completed', '2024-06-01', 'Payment received')")
cursor.execute("INSERT INTO fintech VALUES (2, 1002, 125.00, 'Pending', '2024-06-02', 'Invoice sent')")
cursor.execute("INSERT INTO fintech VALUES (3, 1003, 300.50, 'Failed', '2024-06-03', 'Payment failed')")


## Display all records from the table
print("Inserted records:")
data = cursor.execute("SELECT * FROM fintech")
for row in data:
    print(row)

## Close the connection
connection.commit()
connection.close()