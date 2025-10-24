from tabulate import tabulate
import stdiomask
from db_connection import c, cur, pq
from datetime import datetime

def student_page():
    s="y"
    while s=="y":
        print(" \n 1 FOR LOGIN \n 2 FOR REGISTER \n 3 FOR LOGOUT \n")
        d=int(input("Enter The Choice: "))
        if d==1:
            student_login()
        elif d==2:
            student_register()
        elif d==3:
            s="n"

def student_login():
    Student_user_name=input("Enter The Username: ")
    Student_password= stdiomask.getpass("Enter The Password: ")
    cur=c.cursor()
    sql = "SELECT * FROM student_login  WHERE username = %s AND password = %s;"
    cur.execute(sql, (Student_user_name,Student_password))
    result = cur.fetchone()
    if result:
        print("Login Successfull !! \n")
        a="y"
        while a=="y":
            print("     --STUDENT--")
            print(" 1 FOR VIEWING UPCOMING PROGRAMS \n 2 FOR CHECKING ANY PROGRAM IS THERE IN SPECIFIC DATE \n 3 FOR CHECKING THE INSTRUCTIONS AND BOOKING TIME\n ")
            ch8=int(input("Enter The Choice: "))
            if ch8==1:
                view_upcoming_programs()
            elif ch8==2:
                check_program_by_date()
            elif ch8==3:
                check_program_details()
            a=input("Do You Want To Continue (y/n)?" )
    else:
        print("Invaild Credential")

def view_upcoming_programs():
    try:
        cur = c.cursor()
        cur.execute("select Venue_Name,Programs_On_Venue,Booked_Date from venuebooker where Booking_Details= 'Booked' AND Booked_Date >= CURRENT_DATE;")
        e=cur.fetchall()
        if e:
            headers = [description[0] for description in cur.description]
            print(tabulate(e, headers=headers, tablefmt="grid"))
        else:
            print("No upcoming programs found.")
        c.commit()
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def check_program_by_date():
    try:
        cur = c.cursor()
        date=input("Enter The Date That You Need Check Whether Program Is There Or Not (YYYY-MM-DD): ")
        cur.execute("select Venue_Name,Programs_On_Venue,Booked_Date from venuebooker where  Booking_Details= 'Booked' and  Booked_Date = %s;", (date,))
        e=cur.fetchall()
        if e:
            headers = [description[0] for description in cur.description]
            print(tabulate(e, headers=headers, tablefmt="grid"))
        c.commit()
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def check_program_details():
    print("\n 1 FOR VIEWING ACCORDING TO THE DEPARTMENT \n 2 FOR VIEWING ALL DEPARTMENT \n")
    j=int(input("Enter The Choice: "))
    try:
        cur = c.cursor()
        if j==1:
            b=input("Enter Department Name: ")
            cur.execute("select Venue_Name,Programs_On_Venue,Booked_Date from venuebooker where  Booking_Details= 'Booked' and Department_Name= %s;", (b,))
            e=cur.fetchall()
            if e:
                headers = [description[0] for description in cur.description]
                print(tabulate(e, headers=headers, tablefmt="grid"))
                c.commit()
        elif j==2:
            cur.execute("select Venue_Name,Programs_On_Venue,Booked_Date from venuebooker where  Booking_Details= 'Booked';")
            e=cur.fetchall()
            if e:
                headers = [description[0] for description in cur.description]
                print(tabulate(e, headers=headers, tablefmt="grid"))
            c.commit()
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def student_register():
    try:
        cur = c.cursor()
        e=input("Enter Youruser Name: ")
        g="y"
        while g=="y":  
            k=stdiomask.getpass("Enter The Password: ")
            if len(k) >= 8 and any(char.isdigit() for char in k):
                j="INSERT INTO  student_login VALUES(%s,%s)"
                cur.execute(j, (e, k))
                c.commit()
                print("Registration Successfull !! \n")
                g="n"
            else:
                print("The password Must Be of Length 8 And Should Contain Atleast A Digit \n")
                g="y"
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()