from tabulate import tabulate
import stdiomask
from datetime import datetime,timedelta
from db_connection import c, cur, pq

def admin_page():
    Adminusername = input("Enter The UserName: ")
    Adminpassword = stdiomask.getpass("Enter The Password: ")
    if Adminusername == "roshan.ajin" and Adminpassword == "r15kl46":
        opt = "y"
        while opt.lower() == "y":
            print("     --ADMIN--")
            print(" 1 TO ADD VENUE DETAILS \n 2 UPDATE VENUE DETAILS \n 3 TO DELETE VENUE \n 4 TO VIEW DETAILS  \n 5 TO DELETE A BOOKING \n 6 TO EXIT \n")
            ch1 = int(input("Enter Your Choice: "))
            if ch1 == 1:
                add_venue_details()
            elif ch1 == 2:
                update_venue_details()
            elif ch1 == 3:
                delete_venue()
            elif ch1 == 4:
                view_admin_details()
            elif ch1 == 5:
                delete_booking()

            elif ch1==6:
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
                old_name = input("Enter The Current Venue Name: ").strip()
                new_name = input("Enter The New Venue Name: ").strip()
                cur.execute("UPDATE venuebooker SET Venue_Name=%s WHERE Venue_Name=%s;", (new_name, old_name))
                cur.execute("UPDATE venue_bookings SET venue_name=%s WHERE venue_name=%s;", (new_name, old_name))
                c.commit()
                print(f"Venue name updated from '{old_name}' to '{new_name}' successfully!")
            elif ch2 == 2:
                l = input("Enter The Venue Name For Which You Want To Update Serial Number: ").strip()
                k = int(input("Enter The New Serial Number: "))
                cur.execute("UPDATE venuebooker SET Id=%s WHERE Venue_Name=%s;", (k, l))
                c.commit()
                print("Serial number updated successfully!")

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
        print("\n 1 TO DELETE VENUE BY SERIAL NUMBER \n 2 DELETE VENUE BY VENUE NAME \n ")
        ch3 = int(input("Enter Your Choice: "))
        try:
            if ch3 == 1:
                p = int(input("Enter The Serial Number To Delete: "))
                d= cur.execute("SELECT Venue_Name FROM venuebooker WHERE Id=%s;", (p,))
                venue = cur.fetchone()
                if venue:
                    cur.execute("DELETE FROM venue_bookings WHERE venue_name=%s;", (venue[0],))
                cur.execute("DELETE FROM venuebooker WHERE Id=%s;", (p,))
                
                c.commit()
            elif ch3 == 2:
               p = input("Enter The Venue Name TO Delete: ")
               cur.execute("DELETE FROM venue_bookings WHERE venue_name=%s;", (p,))
               cur.execute("DELETE FROM venuebooker WHERE Venue_Name=%s;", (p,))

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
    """Displays all venues that exist in the system, with seat count and booking summary."""
    try:
        cur = c.cursor()
        cur.execute("""
            SELECT 
                v.Id AS Venue_ID,
                v.Venue_Name AS Venue_Name,
                v.Number_Of_Seats AS Seats,
                COUNT(b.booking_id) AS Total_Bookings
            FROM venuebooker v
            LEFT JOIN venue_bookings b ON v.Venue_Name = b.venue_name
            GROUP BY v.Id, v.Venue_Name, v.Number_Of_Seats
            ORDER BY v.Id;
        """)
        result = cur.fetchall()

        if result:
            headers = [desc[0] for desc in cur.description]
            print(tabulate(result, headers=headers, tablefmt="grid"))
        else:
            print("No venues found in the system.")
    except pq.Error as err:
        print(f"Database Error: {err}")
        c.rollback()
    finally:
        cur.close()
def delete_booking():
    try:
        cur = c.cursor()

        venue_name = input("Enter the venue name: ").strip()
        date_input = input("Enter the booking date (YYYY-MM-DD): ").strip()
        try:
            booking_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print(" Invalid date format. Please use YYYY-MM-DD.")
            return

        cur.execute("""
            SELECT booking_id, department_name, program_name, username
            FROM venue_bookings
            WHERE venue_name = %s AND booked_date = %s;
        """, (venue_name, booking_date))
        record = cur.fetchone()

        if not record:
            print(" No booking found for that venue on that date.")
            return

        print(f"\nBooking found:")
        print(f" - Department: {record[1]}")
        print(f" - Program: {record[2]}")
        print(f" - Booked by: {record[3]}\n")

        confirm = input("Are you sure you want to delete this booking? (y/n): ").lower()
        if confirm == "y":
            cur.execute("DELETE FROM venue_bookings WHERE booking_id = %s;", (record[0],))
            c.commit()
            print("Booking deleted successfully!")
        else:
            print("Deletion cancelled.")

    except pq.Error as err:
        print(f"Database Error: {err}")
        c.rollback()
    finally:
        cur.close()
