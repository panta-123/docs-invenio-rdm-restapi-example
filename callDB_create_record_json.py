import requests
import json
import pymysql  # Assuming you are using MySQL/MariaDB

# Define your database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'username',
    'password': 'password',
    'database': 'your_database'
}

# Function to execute SQL queries and create records.json
def create_records_json():
    # Connect to the database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Example SQL query to fetch data from a table
    query = "SELECT id, name, description FROM your_table"
    cursor.execute(query)
    records = cursor.fetchall()

    # Convert records to JSON format
    records_json = []
    for record in records:
        record_dict = {
            'id': record[0],
            'name': record[1],
            'description': record[2]
        }
        records_json.append(record_dict)

    # Write JSON data to records.json
    with open('records.json', 'w') as json_file:
        json.dump(records_json, json_file)

    # Close database connection
    cursor.close()
    connection.close()

# Create records.json using SQL queries
create_records_json()

# Now you can continue with the rest of your code to upload and publish records
# Make sure to run this entire script as a background process using appropriate tools


