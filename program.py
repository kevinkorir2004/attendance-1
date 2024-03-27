import datetime
import json
import os
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
students_file = "students.txt"
full_students_path = os.path.join(script_dir, students_file)

MONTHS_WITH_31 = ['01', '03', '05', '07', '08', '10', '12']
NUMBER_OF_CLASSES = 24
MIN_PERCENTAGE_TO_PASS = 75
MIN_CLASSES_TO_MISS = (24 * (100-75)) // 100
POSITIVE_CONFIRMATIONS = ['yes', 'y']
ACCEPTED_ATTENDANCE_STATUS = ['p', 'a']
ACTIONS = [
    "Take today's attendance",
    "Add a student",
    "Edit a student's attendance",
    "View a student's attendance",
    "Remove a student",
    "Quit"
]


with open(full_students_path, "r") as infile:
    students = json.load(infile)


def name_or_id(input_string):
    if input_string.isnumeric():
        return 'id'
    else:
        return 'name'

def date_format_verification(date_string):
    if type(date_string) is not str:
        return False
    date_list = date_string.split('-')
    if len(date_list) != 3:
        return False
    if len(date_list[0]) != 4 or len(date_list[1]) != 2 or len(date_list[2]) != 2:
        return False
    if int(date_list[1]) > 12 or int(date_list[2]) > 31:
        return False
    if date_list[1] not in MONTHS_WITH_31:
        if date_list[1] == '02':
            if int(date_list[2]) > 29:
                return False
        else:
            if int(date_list[2]) > 30:
                return False
    return True

def print_single_student_name(student):
    total_indent = 10
    control_space = 3
    print()
    print(student["id"], end='')
    space_between = total_indent - len(str(student["id"]))
    for i in range(max(space_between, control_space)):
        print('.', end='')
    print(student["name"])

def print_names(students_list):
    total_indent = 10
    control_space = 3
    print()
    for student in students_list:
        print(student["id"], end='')
        space_between = total_indent - len(str(student["id"]))
        for i in range(max(space_between, control_space)):
            print('.', end='')
        print(student["name"])
    print()

def print_attendance(student):
    attendance_list = student["attendance"]
    space_between = 4
    print()
    for day in attendance_list:
        print(day["date"], end='')
        for i in range(space_between):
            print('.', end='')
        print(day["status"])
    print()

def print_actions(actions_list):
    for i in range(len(actions_list)):
        print(f"{str(i+1)}. {actions_list[i]}")

def fail_check(students_list):
    for student in students_list:
        sum = 0
        for day in student['attendance']:
            if day['status'] == 'absent':
                sum += 1
        if sum > MIN_CLASSES_TO_MISS:
            student['fail'] = True

def find_student(students_list):
    while True:
        print("Enter quit to quit.")
        identifior = input("Write the student's name or id: ").strip()
        print()
        if identifior.lower() == "quit":
            break
        type_of_identifior = name_or_id(identifior)
        if type_of_identifior == 'id':
            identifior = int(identifior)
        for student in students_list:
            if student[type_of_identifior] == identifior:
                return student
    return None

def get_date():
    date_accepted = False
    while not date_accepted:
        print("\nyyyy-mm-dd")
        date_input = input("Write the date in the above format: ")
        valid_date = date_format_verification(date_input)
        if not valid_date:
            continue
        print("\n" , date_input)
        date_confirmation = input("Is that the right date? [y/n]: ").strip()
        date_accepted = date_confirmation.lower() in POSITIVE_CONFIRMATIONS
    return date_input




def take_attendance(students_list):
    date_to_use = datetime.datetime.now().date()
    print(date_to_use)
    print("Enter n to choose another date.")
    confirm_date = input("Do you want to take today's attendance? [y/n]: ")
    if confirm_date not in POSITIVE_CONFIRMATIONS:
        date_to_use = get_date()
    print()
    print("Enter p for present, and a for absent.")
    for student in students_list:
        updated_attendance = False
        while not updated_attendance:
            print_single_student_name(student)
            current_status = input("[p/a]: ").strip()
            updated_attendance = current_status.lower() in ACCEPTED_ATTENDANCE_STATUS

def view_student_attendance(students_list):
    student = find_student(students_list)
    if student == None:
        return
    print_attendance(student)


while True:
    print("\nWhat would you like to do?")
    print_actions(ACTIONS)
    action_input = input("Enter a number: ")
    print()
    if not action_input.isnumeric():
        print("You should enter a number.")
        time.sleep(.8)
        continue
    action_id = int(action_input)
    if action_id < 1 or action_id > len(ACTIONS):
        print("Enter one of the numbers above.")
        time.sleep(.8)
        continue
    elif action_id == 1:
        take_attendance(students)
        break
    elif action_id == 4:
        view_student_attendance(students)
        break
    elif action_id == 6:
        break
    break

# with open(full_students_path, "w") as outfile:
#     students_string = json.dumps(students, indent=4)
#     outfile.write(students_string)



# date = datetime.datetime.now().date()
# print(date)