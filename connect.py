import mysql.connector

def sqlcon():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="220905@Ig",
        database="students"
    )
    return conn