from tabulate import tabulate
import stdiomask
from db_connection import c, cur, pq

def admin_page():
    Adminusername = input("Enter The UserName: ")
    Adminpassword = stdiomask.getpass("Enter The Password: ")
    if Adminusername == "roshan.ajin" and Adminpassword == "r15kl46":
        opt = "y"
        while opt.lower() == "y":
            print("     --ADMIN--")
            print(" 1 TO ADD VENUE DETAILS \n 2 UPDATE VENUE DETAILS \n 3 TO DELETE VENUE \n 4 TO VIEW DETAILS  \n 5 TO EXIT \n")
            ch1 = int(input("Enter Your Choice: "))
            if ch1 == 1:
                add_venue_details()
            elif ch1 == 2:
                update_venue_details()
            elif ch1 == 3:
                delete_venue()
            elif ch1 == 4:
                view_admin_details()
            elif ch1==5:
                opt ='n'
            else:
                print("Invalid choice.")
    else:
        print("Invalid Admin Username or Password.")

def add_venue_details():
    f = "y"
    while f.lower() == "y":
        cur = c.cursor()
        a = "Available"
        d = int(input("Enter the Serial Number: "))
        venue = input("Enter The Venue name: ")
        seat=int(input("Enter The Number Of Seats: "))
        q = "INSERT INTO venuebooker (Id, Venue_Name, Booking_Details, Number_Of_Seats) VALUES (%s, %s, %s, %s);"
        try:
            cur.execute(q, (d, venue, a, seat))
            c.commit()
        except pq.Error as err:
            print(f"Error: {err}")
            c.rollback()
        finally:
            cur.close()
        f = input("Do You Want To Add More Venue Details (y/n)? ").lower()

def update_venue_details():
    print("\n 1 TO UPDATE VENUE_NAME \n 2 TO UPDATE THE SERIAL NUMBER \n")
    a = "y"
    while a.lower() == "y":
        cur = c.cursor()
        ch2 = int(input("Enter Your Choice: "))
        try:
            if ch2 == 1:
                b = input("Enter The New Venue Name: ")
                j = int(input("Enter The Serial Number: "))
                u = "UPDATE venuebooker SET Venue_Name=%s where Id =%s;"
                cur.execute(u, (b, j))
                c.commit()
            elif ch2 == 2:
                l = input("Enter The Venue Name For Which You Want To Update Serial Number: ")
                k = int(input("Enter The New Serial Number: "))
                u= "UPDATE venuebooker SET Id=%s where Venue_Name=%s;"
                cur.execute(u, (k, l))
                c.commit()
            else:
                print("Invalid choice.")
        except pq.Error as err:
            print(f"Error: {err}")
            c.rollback()
        finally:
            cur.close()
        a = input("Do You Want To Update More Details (y/n)? ").lower()

def delete_venue():
    t = "y"
    while t == "y":
        cur=c.cursor()
        print("\n 1 TO DELETE VENUE BY SERIAL NUMBER \n 2 DELETE VENUE BY VENUE NAME \n 3 DELETE THE DETAILS OF BOOKING \n")
        ch3 = int(input("Enter Your Choice: "))
        try:
            if ch3 == 1:
                p = int(input("Enter The Serial Number To Delete: "))
                d= "DELETE FROM venuebooker where Id=%s;"
                cur.execute(d, (p,))
                c.commit()
            elif ch3 == 2:
                p = input("Enter The Venue Name TO Delete: ")
                d= "DELETE FROM venuebooker where Venue_Name=%s;"
                cur.execute(d, (p,))
                c.commit()
            elif ch3 == 3:
                l=None
                j=int(input("Enter The Serial Number: "))
                a="Available"
                d="UPDATE venuebooker SET Booking_Details = %s WHERE Id=%s;"
                b="UPDATE venuebooker SET Booked_Date  = %s WHERE Id=%s;"
                e="UPDATE venuebooker SET Programs_On_Venue = %s WHERE Id=%s;"
                f="UPDATE venuebooker SET Department_Name  = %s WHERE Id=%s;"
                p="UPDATE venuebooker SET Username = %s WHERE Id=%s;"
                ins="UPDATE venuebooker SET Instructions=%s where Id=%s;"
                cur.execute(ins, (l, j))
                cur.execute(p, (l, j))
                cur.execute(d, (a, j))
                cur.execute(b, (l, j))
                cur.execute(e, (l, j))
                cur.execute(f, (l, j))
                c.commit()
            
            else:
                print("Invalid choice.")
        except pq.Error as err:
            print(f"Error: {err}")
            c.rollback()
        finally:
            if 'cur' in locals() and cur is not None:
                cur.close()
        t = input("Do You Want To Delete More Venue (y/n)? ").lower()

def view_admin_details():
    try:
        cur = c.cursor()
        cur.execute("select  Id,Venue_Name,Booked_Date,Department_Name from venuebooker;")
        e = cur.fetchall()
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