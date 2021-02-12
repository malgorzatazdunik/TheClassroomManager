import sqlite3
import time
from datetime import date

from classes import students

def get_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def main():
    conn, cursor = get_db("database.db")

    sql = '''create table if not exists students (
    id int,
    first char,
    last char,
    dob int)'''

    cursor.execute(sql)

    sql2 = '''create table if not exists grades (
    student_id int,
    test char,
    grade int)'''

    cursor.execute(sql2)
    conn.commit()

    while True:
        c = menu()
        if c=="5":
            print ("Goodbye")
            conn.commit()
            conn.close()
            break
        do_option(c,cursor)
        conn.commit()

def get_choice():
    while True:
        c = input("Choice [1-5]: ")
        if not c or c[0] not in "12345":
            print ("{} is not valid.".format(c))
        else:
            return c[0]


def do_option(c, cursor):
    if c=="1":
        students.add_student(cursor)
    elif c=="2":
        students.delete_student(cursor)
    elif c=="3":
        students.print_students(cursor)
    elif c=="4":
        students.print_student(cursor)

def menu():
    print("Options:")
    print("1.Add student\n\
    2. Delete a student\n\
    3. Print all students\n\
    4. Print one student\n\
    5. Quit")
    c = get_choice()
    return c

if __name__ == '__main__':
    main()
