import pandas as pd
import mysql.connector

# Database connection parameters
db_config = {
    'host': 'localhost3306',  # Change as needed
    'user': 'root',  # Change as needed
    'password': 12345,  # Change as needed
    'database': 'project'  # Change as needed
}

# Read the CSV file
csv_file_path = 'path_to_your_file.csv'  # Change to your CSV file path
data = pd.read_csv(csv_file_path)

# Connect to the database
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Prepare the SQL insert statement
    insert_query = """
    INSERT INTO DESTINATIONS (name, state, type, popularity, best_time_to_visit)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Iterate over the DataFrame and insert each row into the database
    for index, row in data.iterrows():
        cursor.execute(insert_query, (
            row['Name'],
            row['State'],
            row['Type'],
            row['Popularity'],
            row['BestTimeToVisit']
        ))

    # Commit the transaction
    connection.commit()
    print("Data inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

# CREATE TABLE ATTRACTIONS (

# id INT AUTO INCREMENT PRIMARY KEY,

# destination_id INT NOT NULL,

# name VARCHAR(255) NOT NULL,

# state varchar(255) NOT NULL,

# category VARCHAR(255),

# rating DECIMAL (3,2),

# FOREIGN KEY (destination_id) REFERENCES DESTINATIONS (id) ON DELETE CASCADE

# );