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
    CREATE TABLE IF NOT EXISTS venue_bookings (
    booking_id SERIAL PRIMARY KEY,
    venue_name VARCHAR(255) REFERENCES venuebooker(Venue_Name),
    booked_date DATE NOT NULL,
    department_name VARCHAR(255),
    username VARCHAR(255),
    program_name VARCHAR(255),
    program_time VARCHAR(50),
    instructions TEXT
);
"""
    
    commands = table_creation_commands.split(';')
    for command in commands:
        if command.strip():
            cur.execute(command)
            
    c.commit()
    cur.execute("""
    DELETE FROM venue_bookings
    WHERE booked_date < CURRENT_DATE;
""")
    c.commit()

except pq.Error as err:
    print(f"Error connecting to PostgreSQL: {err}")
    exit()

def close_connection():
    if 'c' in locals():
        c.close()