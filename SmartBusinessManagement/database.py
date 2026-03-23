import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="*****",   #your password 
        database="smart_business_db"
    )
    return connection
