from tabulate import tabulate
import stdiomask
from datetime import datetime,timedelta
from db_connection import c, cur, pq

def department_page():
    s="y"
    while s=="y":
        print(" \n 1 FOR LOGIN \n 2 FOR REGISTER \n 3 FOR LOGOUT \n")
        d=int(input("Enter The Choice: "))
        if d==1:
            department_login()
        elif d==2:
            department_register()
        elif d==3:
            s="n"

def department_login():
    Departmentlogin=input("Enter The Username: ")
    Departmentpassword= stdiomask.getpass("Enter The Password: ")
    cur=c.cursor()
    sql = "SELECT * FROM departmentlogin WHERE username = %s AND password = %s;"
    cur.execute(sql, (Departmentlogin, Departmentpassword))
    result = cur.fetchone()
    if result:
        print("Login Successfull !! \n")
        a="y"
        while a=="y":
            print("     --DEPARMENT--")
            print(" 1 FOR VIEWING VENUE AVAILABLE \n 2 FOR VENUE BOOKING \n 3 FOR VIEW PROGRAMS ON VENUE \n 4 FOR CHANGING VENUE \n 5 FOR UPDATEING PARTICIPATION DETAILS \n")
            ch7=int(input("Enter The Choice: "))
            if ch7==1:
                view_available_venues()
            elif ch7==2:
                book_venue(Departmentlogin)
            elif ch7==3:
                view_booked_programs()
            elif ch7==4:
                change_venue(Departmentlogin)
            elif ch7==5:
                update_participation_details()
            a=input("Do You Want To Continue In Doing Opertaions In Department (y/n)?" )
    else:
        print("Invalid Department Username or Password.")

def view_available_venues():
    try:
        cur = c.cursor()
        cur.execute("select Venue_Name,Number_Of_Seats from venuebooker where  Booking_Details= 'Available';")
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
            
def book_venue(Departmentlogin):
    try:
        cur=c.cursor()
        no_seats=int(input("Enter The Number Of Seats That You Need: "))
        cur.execute("select Venue_Name,Number_Of_Seats from venuebooker where  Booking_Details= 'Available' and Number_Of_Seats >=%s;", (no_seats,))
        e=cur.fetchall()
        if e:
            headers = [description[0] for description in cur.description]
            print(tabulate(e, headers=headers, tablefmt="grid"))
        c.commit()
        
        curdate=datetime.now().date()
        mindate=curdate+timedelta(days=14)
        r=input('Enter The Date for which you want to book:("YYYY-MM-DD"): ')
        j=datetime.strptime(r, '%Y-%m-%d').date()
        if curdate < j <=mindate:
            print("You Could Only Book The Venue Available \n")
            l=input("Enter The Venuename: ")
            p=input("Enter The Department Name: ")
            h=input("Enter  Your Program Which Is Going TO Conducted On The Venue: ")
            time=input('Enter The Time Of Program: ')
            inst=input("Enter The Instructions Or Rules For The Program: ")
            
            g="Booked"
            i="Available"
            a="UPDATE  venuebooker SET  Booked_Date=%s where Venue_Name =%s and  Booking_Details=%s; "
            z="UPDATE  venuebooker SET  Programs_On_Venue =%s where Venue_Name =%s and  Booking_Details=%s; "
            y="UPDATE  venuebooker SET   Department_Name=%s where Venue_Name =%s and  Booking_Details=%s; "
            o="UPDATE venuebooker SET Booking_Details=%s where Venue_Name =%s; "
            b="UPDATE venuebooker SET  Username=%s where Venue_Name =%s; "
            kp="UPDATE venuebooker SET  Program_Time=%s where Venue_Name =%s; "
            ins="UPDATE  venuebooker SET Instructions=%s where Venue_Name =%s and  Booking_Details=%s; "
            cur.execute(kp, (time, l))
            cur.execute(ins, (inst, l, i))
            cur.execute(b, (Departmentlogin, l))
            cur.execute(a, (r, l, i))
            cur.execute(z, (h, l, i))
            cur.execute(y, (p, l, i))
            cur.execute(o, (g, l))
            c.commit()
        else:
            print("You Can Only Book Before 14 Days")
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def view_booked_programs():
    try:
        cur = c.cursor()
        cur.execute("select  Venue_Name,Programs_On_Venue  from venuebooker where  Booking_Details= 'Booked';")
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

def change_venue(Departmentlogin):
    try:
        cur=c.cursor()
        no_seats=int(input("Enter The Number Of Seats That You Need: "))
        cur.execute("select Venue_Name,Number_Of_Seats from venuebooker where  Booking_Details= 'Available' and Number_Of_Seats >=%s;", (no_seats,))
        e=cur.fetchall()
        if e:
            headers = [description[0] for description in cur.description]
            print(tabulate(e, headers=headers, tablefmt="grid"))
        c.commit()
        
        curdate=datetime.now().date()
        mindate=curdate+timedelta(days=14)
        bookingdate=input('Enter The Date for which you want to book:("YYYY-MM-DD"): ')
        j=datetime.strptime(bookingdate, '%Y-%m-%d').date()
        
        if curdate < j <=mindate:
            venuename=input("Enter The Venuename That You Have ALready Booked: ")  
            l=None
            ak="Available"
            de="UPDATE venuebooker SET Booking_Details=%s WHERE Venue_Name=%s and  Username=%s;"
            b="UPDATE venuebooker SET Booked_Date=%s WHERE Venue_Name=%s and Username=%s;"
            ef="UPDATE venuebooker SET Programs_On_Venue=%s WHERE Venue_Name=%s and Username=%s;"
            f="UPDATE venuebooker SET Department_Name=%s WHERE Venue_Name=%s and Username=%s;"
            ins="UPDATE venuebooker SET Instructions=%s where Venue_Name =%s;"
            p="UPDATE venuebooker SET Username=%s WHERE Venue_Name=%s ;"
            jk="UPDATE venuebooker SET Program_Time=%s WHERE Venue_Name=%s ;"
            cur.execute(ins, (l, venuename))
            cur.execute(de, (ak, venuename, Departmentlogin))
            cur.execute(b, (l, venuename, Departmentlogin))
            cur.execute(ef, (l, venuename, Departmentlogin))
            cur.execute(f, (l, venuename, Departmentlogin))
            cur.execute(p, (l, venuename))
            cur.execute(jk, (l, venuename))
            
            newvenue=input("Enter The  New Venuename That You Need To Book: ")
            departmentname=input("Enter The Department Name: ")
            programname=input("Enter  Your Program Which Is Going TO Conducted On The Venue: ")
            time=input('Enter The Time Of Program: ')
            inst=input("Enter The Instructions Or Rules For The Program: ")
            g="Booked"
            ab="UPDATE  venuebooker SET  Booked_Date=%s where Venue_Name=%s and  Booking_Details=%s; "
            z="UPDATE  venuebooker SET  Programs_On_Venue=%s where Venue_Name=%s and  Booking_Details=%s; "
            y="UPDATE  venuebooker SET   Department_Name=%s where Venue_Name=%s and  Booking_Details=%s; "
            ins="UPDATE  venuebooker SET   Instructions=%s where Venue_Name =%s and  Booking_Details=%s; "
            o="UPDATE venuebooker SET Booking_Details=%s where Venue_Name=%s; "
            bk="UPDATE venuebooker SET  Username=%s where Venue_Name=%s; "
            kp="UPDATE venuebooker SET  Program_Time=%s where Venue_Name =%s; "
            cur.execute(kp, (time, newvenue))
            cur.execute(ins, (inst, newvenue, ak))
            cur.execute(bk, (Departmentlogin, newvenue))
            cur.execute(ab, (bookingdate, newvenue, ak))
            cur.execute(z, (programname, newvenue, ak))
            cur.execute(y, (departmentname, newvenue, ak))
            cur.execute(o, (g, newvenue))
            c.commit()
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def update_participation_details():
    try:
        cur = c.cursor()
        l=int(input("Enter The Serial Number: "))
        f=int(input("Enter The Participation Number: "))
        h=input("Enter The Department Name: ")
        g=input("Enter The Program Name Conducted: ")
        v="INSERT INTO department (Id,Particpation,Department_Name,Program_Name) VALUES(%s,%s,%s,%s);"
        cur.execute(v, (l, f, h, g))
        c.commit()
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()

def department_register():
    try:
        cur = c.cursor()
        e=input("Enter New Department Name: ")
        g="y"
        while g=="y":  
            k=stdiomask.getpass("Enter Department Password: ")
            if len(k) >= 8 and any(char.isdigit() for char in k):
                j="INSERT INTO  departmentlogin VALUES(%s,%s)"
                cur.execute(j, (e, k))
                c.commit()
                print("Registration Successfull !!")
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