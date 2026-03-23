import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="manognya@200624",
        database="smart_business_db"
    )
    return connection
