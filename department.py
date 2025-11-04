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
            print(" 1 FOR VIEWING VENUE AVAILABLE \n 2 FOR VENUE BOOKING \n 3 FOR VIEW PROGRAMS ON VENUE \n 4 FOR CHANGING VENUE \n 5 FOR UPDATEING PARTICIPATION DETAILS \n 6 FOR CANCELLING A BOOKING \n")
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
            elif ch7 == 6:
                cancel_booking(Departmentlogin)

            a=input("Do You Want To Continue In Doing Opertaions In Department (y/n)?" )
    else:
        print("Invalid Department Username or Password.")

def view_available_venues():
    """Displays all venues that are free on a given date."""
    try:
        cur = c.cursor()
        date_input = input("Enter the date to check availability (YYYY-MM-DD): ").strip()
        try:
            check_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        try:
            required_seats = int(input("Enter minimum number of seats required (or 0 to skip): "))
        except ValueError:
            print(" Invalid seat number.")
            return
        if required_seats > 0:
            cur.execute("""
                SELECT v.Venue_Name, v.Number_Of_Seats
                FROM venuebooker v
                WHERE v.Venue_Name NOT IN (
                    SELECT venue_name FROM venue_bookings WHERE booked_date = %s
                )
                AND v.Number_Of_Seats >= %s
                ORDER BY v.Number_Of_Seats DESC;
            """, (check_date, required_seats))
        else:
            cur.execute("""
                SELECT v.Venue_Name, v.Number_Of_Seats
                FROM venuebooker v
                WHERE v.Venue_Name NOT IN (
                    SELECT venue_name FROM venue_bookings WHERE booked_date = %s
                )
                ORDER BY v.Number_Of_Seats DESC;
            """, (check_date,))

        rows = cur.fetchall()
        if rows:
            headers = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print(" No available venues found for that date.")

    except pq.Error as err:
        print(f"Database Error: {err}")
        c.rollback()
    finally:
        cur.close()


            
def book_venue(Departmentlogin):
    try:
        cur = c.cursor()
        curdate = datetime.now().date()
        mindate = curdate + timedelta(days=14)
        booking_date_input = input('Enter the date you want to book (YYYY-MM-DD): ')
        try:
            booking_date = datetime.strptime(booking_date_input, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        if not (curdate < booking_date <= mindate):
            print("You can only book for dates from tomorrow up to 14 days ahead.")
            return
        try:
            required_seats = int(input("Enter the number of seats you need: "))
            if required_seats <= 0:
                print("Number of seats must be positive.")
                return
        except ValueError:
            print("Invalid number entered.")
            return
        cur.execute("""
            SELECT v.Venue_Name, v.Number_Of_Seats
            FROM venuebooker v
            WHERE v.Number_Of_Seats >= %s
            AND v.Venue_Name NOT IN (
                SELECT venue_name FROM venue_bookings WHERE booked_date = %s
            )
            ORDER BY v.Venue_Name;
        """, (required_seats, booking_date))
        available_venues = cur.fetchall()

        if not available_venues:
            print("No venues available on that date with enough seats.")
            return
        headers = [description[0] for description in cur.description]
        print("\nVenues available on", booking_date_input, "with at least", required_seats, "seats:")
        print(tabulate(available_venues, headers=headers, tablefmt="grid"))
        venue_choice = input("\nEnter the Venue Name you want to book: ").strip()
        valid_venues = [row[0] for row in available_venues]
        if venue_choice not in valid_venues:
            print("Invalid venue name or not available.")
            return
        dept_name = input("Enter your Department Name: ").strip()
        program = input("Enter the Program Name: ").strip()
        program_time = input("Enter the Program Time: ").strip()
        instructions = input("Enter any Instructions or Rules (or press Enter to skip): ").strip()
        cur.execute("""
            INSERT INTO venue_bookings
                (venue_name, booked_date, department_name, username, program_name, program_time, instructions)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (venue_choice, booking_date, dept_name, Departmentlogin, program, program_time, instructions))
        c.commit()

        print(f"Venue '{venue_choice}' successfully booked for {booking_date_input}.")

    except pq.Error as err:
        print(f"Database Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()


def view_booked_programs():
    """Displays all programs that are currently booked on venues."""
    try:
        cur = c.cursor()
        cur.execute("""
            SELECT 
                venue_name AS Venue,
                program_name AS Program,
                department_name AS Department,
                booked_date AS Date,
                program_time AS Time
            FROM venue_bookings
            WHERE booked_date >= CURRENT_DATE
            ORDER BY booked_date;
        """)
        records = cur.fetchall()

        if records:
            headers = [desc[0] for desc in cur.description]
            print(tabulate(records, headers=headers, tablefmt="grid"))
        else:
            print("No booked programs found.")
    except pq.Error as err:
        print(f"Error: {err}")
        c.rollback()
    finally:
        cur.close()


def change_venue(Departmentlogin):
    try:
        cur = c.cursor()
        old_venue = input("Enter the venue name you have already booked: ").strip()
        old_date_input = input("Enter the booked date (YYYY-MM-DD): ").strip()

        try:
            old_date = datetime.strptime(old_date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid old date format. Please use YYYY-MM-DD.")
            return
        cur.execute("""
            SELECT booking_id FROM venue_bookings
            WHERE venue_name = %s AND booked_date = %s AND username = %s;
        """, (old_venue, old_date, Departmentlogin))
        old_record = cur.fetchone()

        if not old_record:
            print("No matching booking found for you on that date.")
            return
        curdate = datetime.now().date()
        mindate = curdate + timedelta(days=14)
        new_date_input = input("Enter the new date for booking (YYYY-MM-DD): ").strip()
        try:
            new_date = datetime.strptime(new_date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if not (curdate < new_date <= mindate):
            print("You can only book within 14 days from today.")
            return
        try:
            required_seats = int(input("Enter the number of seats you need: "))
            if required_seats <= 0:
                print("Number of seats must be positive.")
                return
        except ValueError:
            print("Invalid seat number.")
            return
        cur.execute("""
            SELECT v.Venue_Name, v.Number_Of_Seats
            FROM venuebooker v
            WHERE v.Number_Of_Seats >= %s
            AND v.Venue_Name NOT IN (
                SELECT venue_name FROM venue_bookings WHERE booked_date = %s
            )
            ORDER BY v.Venue_Name;
        """, (required_seats, new_date))
        available_venues = cur.fetchall()
        if not available_venues:
            print("No venues available on that date with enough seats.")
            return
        headers = [description[0] for description in cur.description]
        print(f"\nVenues available on {new_date_input} with at least {required_seats} seats:")
        print(tabulate(available_venues, headers=headers, tablefmt="grid"))
        new_venue = input("\nEnter the new venue name to book: ").strip()
        valid_venues = [row[0] for row in available_venues]
        if new_venue not in valid_venues:
            print("Invalid or unavailable venue selected.")
            return

        dept_name = input("Enter your Department Name: ").strip()
        program_name = input("Enter the Program Name: ").strip()
        program_time = input("Enter the Program Time: ").strip()
        instructions = input("Enter any Instructions or Rules (or press Enter to skip): ").strip()
        cur.execute("DELETE FROM venue_bookings WHERE booking_id = %s;", (old_record[0],))
        cur.execute("""
            INSERT INTO venue_bookings
                (venue_name, booked_date, department_name, username, program_name, program_time, instructions)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (new_venue, new_date, dept_name, Departmentlogin, program_name, program_time, instructions))
        c.commit()

        print(f" Booking changed successfully!")
        print(f"Old booking: {old_venue} on {old_date_input}")
        print(f"New booking: {new_venue} on {new_date_input}")

    except pq.Error as err:
        print(f"Database Error: {err}")
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
def cancel_booking(Departmentlogin):
    try:
        cur = c.cursor()
        venue_name = input("Enter the venue name to cancel: ").strip()
        date_input = input("Enter the booked date (YYYY-MM-DD): ").strip()
        try:
            booking_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
        cur.execute("""
            SELECT booking_id FROM venue_bookings
            WHERE venue_name = %s AND booked_date = %s AND username = %s;
        """, (venue_name, booking_date, Departmentlogin))
        record = cur.fetchone()

        if not record:
            print("No matching booking found for you on that date.")
            return
        confirm = input(f"Are you sure you want to cancel booking for '{venue_name}' on {date_input}? (y/n): ").lower()
        if confirm == "y":
            cur.execute("DELETE FROM venue_bookings WHERE booking_id = %s;", (record[0],))
            c.commit()
            print(f"Booking for '{venue_name}' on {date_input} cancelled successfully.")
        else:
            print("Cancellation aborted.")

    except pq.Error as err:
        print(f"Database Error: {err}")
        c.rollback()
    finally:
        if 'cur' in locals() and cur is not None:
            cur.close()
