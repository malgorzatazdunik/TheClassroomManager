import sqlite3
import time
from datetime import date


d = date(2013, 6, 30)
d.toordinal()

def add_student(cursor):
    student_id = input("Student ID: ")
    last = input("Last name: ")
    first = input("First name: ")
    dob = input("DOB [mm/dd/yyyy]: ")

    #student_id = check_id(student_id, cursor)

    while True:
        try:
            d = time.strptime(dob, "%m %d %Y")

        except:
            print ("{} isn't valid.".format(dob))
            dob = input("DOB [mm dd yyy]: ")
        else:
            dob = date(d.tm_year, d.tm_mon, d.tm_mday)
            dob_ord = dob.toordinal()
            break

    sql = '''insert into students (id, first, last, dob) values (:st_id, :st_first, :st_last, :st_dob)'''

    values = {"st_id": student_id, "st_last": last, "st_first": first, "st_dob": dob_ord}
    cursor.execute(sql, values)

def delete_student(cursor):
    print_students(cursor)
    student_id = input("ID: ")
    student_id = check_id(student_id, cursor)
    values = {"st_id": student_id}

    sql = '''delete from students where id=:st_id'''
    cursor.execute(sql,values)

    sql = '''delete from grades where student_id=:st_id'''
    cursor.execute(sql, values)
    print ("Deleted")


def print_students(cursor):
    sql = '''select last, first, id from students'''
    result = cursor.execute(sql)
    students = result.fetchall()

    for last, first, s_id in students:
        print("{last}, {first}: {s_id}".format(last=last,first=first,s_id=s_id))

def print_student(cursor):
    sql = '''select id, first, last, dob from students where id=:st_id'''
    student_id = input("ID: ")
    student_id = check_id(student_id, cursor)
    result = cursor.execute(sql, {"st_id": student_id})

    student_id, first, last, dob = result.fetchone()
    dob = date.fromordinal(dob)

    print("{last}, {first}: {student_id}, {dob}".format(last=last,first=first,student_id=student_id,dob=dob))

def add_grade(cursor):
    student_id = input("ID: ")
    student_id = check_id(student_id, cursor)
    test = input("Test: ")
    grade = input("Grade: ")

    sql = '''insert into grades (student_id, test, grade) values (:st_id, :st_test, :st_grade)'''
    values = {"st_id": student_id, "st_test": test, "st_grade": grade}
    cursor.execute(sql, values)

def delete_grade(cursor):
    student_id = input("ID: ")
    student_id = check_id(student_id, cursor)

    values = {"st_id": student_id}
    sql = '''select * from grades where student_id =:st_id'''
    result = cursor.execute(sql, values)
    for id, test, grade in result:
        print("Student id: {id}, Test: {test}, Grade: {grade}".format(id=id, test=test, grade=grade))

    test = input("Select test to delete: ")
    values = {"st_id": student_id, "st_test":test}

    sql = '''delete from grades where student_id =:st_id and test=:st_test'''
    cursor.execute(sql,values)
    print("Deleted!")


def print_report_card(cursor):
    student_id = input("ID: ")
    student_id = check_id(student_id, cursor)

    values = {"st_id": student_id}

    sql = '''select * from grades where student_id=:st_id'''
    result = cursor.execute(sql, values).fetchall()

    sum = 0
    num = 0

    for id, test, grade in result:
        print("Student id: {id}, Test: {test}, Grade: {grade}".format(id=id, test=test, grade=grade))
        sum += int(grade)
        num += 1

    if sum == 0:
        print("No grades")
        return

    print("Average: ", sum/num)

def print_all_grades(cursor):
    sql = '''select * from grades'''
    result = cursor.execute(sql).fetchall()

    for id, test, grade in result:
        print("Student id: {id}, Test: {test}, Grade: {grade}".format(id=id, test=test, grade=grade))

def check_id(student_id, cursor):
    sql = '''select id from students'''
    result = cursor.execute(sql).fetchall()

    for id in result:
        if int(student_id) in id:
            print("id found!")
            return student_id

    student_id = input("Invalid input. ID: ")
    student_id = check_id(student_id, cursor)
