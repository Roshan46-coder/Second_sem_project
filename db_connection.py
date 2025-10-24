import psycopg2 as pq
from datetime import datetime,timedelta
import stdiomask

try:
    c = pq.connect(host="localhost",
                   user="postgres",
                   password="root",
                   database="venuebooker")
    
    cur = c.cursor()
    
    table_creation_commands = """
    CREATE TABLE IF NOT EXISTS venuebooker (
        Id INT PRIMARY KEY,
        Venue_Name VARCHAR(255) UNIQUE NOT NULL,
        Booking_Details VARCHAR(50) NOT NULL,
        Number_Of_Seats INT,
        Booked_Date DATE,
        Programs_On_Venue VARCHAR(255),
        Department_Name VARCHAR(255),
        Username VARCHAR(255),
        Instructions TEXT,
        Program_Time VARCHAR(50)
    );
    CREATE TABLE IF NOT EXISTS departmentlogin (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS student_login (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS department (
        Id INT PRIMARY KEY,
        Particpation INT,
        Department_Name VARCHAR(255),
        Program_Name VARCHAR(255)
    );
    """
    
    commands = table_creation_commands.split(';')
    for command in commands:
        if command.strip():
            cur.execute(command)
            
    c.commit()

    d = "UPDATE venuebooker SET Booking_Details='Available',Booked_Date=NULL,Programs_On_Venue=NULL,Department_Name=NULL,Username=NULL,Instructions=NULL,Program_Time=NULL WHERE Booked_Date < CURRENT_DATE;"
    cur.execute(d)
    c.commit()

except pq.Error as err:
    print(f"Error connecting to PostgreSQL: {err}")
    exit()

def close_connection():
    if 'c' in locals():
        c.close()