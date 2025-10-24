from admin import admin_page
from department import department_page
from student import student_page
from db_connection import close_connection

def main_menu():
    k="y"
    while k=="y":
        print("     --LOGIN--")
        print(" 1 ADMIN PAGE \n 2 DEPARTMENT PAGE\n 3 STUDENT PAGE \n 4 TO EXIT \n")
        ch = int(input("Enter The choice: "))
        if ch == 1:
            admin_page()
        elif ch==2:
            department_page()
        elif ch==3:
            student_page()                 
        elif ch==4:
            k="n"                  
    close_connection()

if __name__ == '__main__':
    main_menu()