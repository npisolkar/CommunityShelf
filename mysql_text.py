import mysql.connector

# Replace these with your MySQL server information
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Co!!ege3oard2",
    "database": "community_shelf",
}

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Connected to MySQL")
except mysql.connector.Error as err:
    print(f"Error: {err}")
#finally:

cursor = connection.cursor()


cursor.execute("""INSERT into users (name, email, phoneNumber, address, zip, password) values 
        ("JamesB", "jamesb@purdue.edu", "3025889267", "881 Brintons Bridge Road", "19382", "JamesPassword" )""")
connection.commit()

connection.close()




