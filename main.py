def read_file(source_file):
    list_of_tuples = []
    with open(source_file) as file:
        for line in file.readlines():
            line = line.strip().split(',')
            list_of_tuples.append(line)
    return list_of_tuples


def write_file(data, destination_file):
    with open(destination_file, "w") as file:
        for line in data:
            file.write(','.join(line) + '\n')


def print_headers():
    print("{: ^5}|{: ^11}|{: ^15}|{: ^43}|{: ^15}|{: ^12}|{: ^15}".format("CRN",
                                                                          "Course Code",
                                                                          "Section Number",
                                                                          "Course Name",
                                                                          "Instructor Name",
                                                                          "Section Size",
                                                                          "Available Seats"))


def print_course_details(course):
    print("{: ^5}|{: ^11}|{: ^15}|{: ^43}|{: ^15}|{: ^12}|{: ^15}".format(course[0],
                                                                          course[1],
                                                                          course[2],
                                                                          course[3],
                                                                          course[4],
                                                                          course[5],
                                                                          str(int(course[-2]) - int(course[-1]))))


def print_courses_info(source_file):
    data = read_file(source_file)
    print_headers()
    for course in data:
        print_course_details(course)


def search_course(source_file):
    data = read_file(source_file)
    choice = input('1. Search by name\n2. Search by course code\n3. Search by course number\nEnter choice: ')
    if choice not in ['1', '2', '3']:
        print("Invalid choice.")
        return
    found = False
    if choice == '1':
        name = input("Enter name: ").lower()
        print_headers()
        for course in data:
            if name in course[3].lower():
                found = True
                print_course_details(course)
    elif choice == '2':
        code = input("Enter course code: ").lower()
        print_headers()
        for course in data:
            if code == course[1].lower():
                found = True
                print_course_details(course)
    else:
        course_number = input("Enter course number: ").lower()
        print_headers()
        for course in data:
            if course_number == course[0].lower():
                found = True
                print_course_details(course)

    if not found:
        print("No course found.")


def add_courses(source_file):
    data = read_file(source_file)
    course_numbers = [course[0] for course in data]
    course = []
    course_number = input("Enter course number: ")
    if course_number in course_numbers:
        print("Serial Number already exists")

    if not course_number.isnumeric() or len(course_number) != 5:
        print("The course number isn't an integer, or it's not 5 digits")
        return

    course_code = input("Enter course code: ")
    if len(course_code) == 0:
        print("The course code cannot be empty.")
        return

    section = input("Enter section number: ")
    if int(section) < 1:
        print("Section number must be positive and non-empty")
        return

    course_name = input("Enter course name: ")
    if len(course_name) == 0:
        print("Course name cannot be empty.")
        return

    instructor = input("Enter instructor name: ")
    if len(instructor) == 0:
        print("Instructor name cannot be empty.")
        return

    size = input("Enter section size: ")
    if int(size) < 1:
        print("Section size must be positive and non-empty")
        return


    course.extend([course_number,course_code,section,course_name, instructor,size,'0'])
    data.append(course)
    write_file(data, source_file)
    print("Course has been added successfully!")


def remove_courses(source_file):
    data = read_file(source_file)
    course_numbers = [course[0] for course in data]

    while True:
        course_number = input("Enter course number: ")

        if course_number in course_numbers:
            break
        else:
            print("Course does not exist")

    print_headers()
    for i, course in enumerate(data):
        if course_number == course[0]:
            print_course_details(course)
            if 'y' == input(f"Do you want to remove the course ({course_number})? [Y/N] ").lower():
                if int(course[-1]) == 0:
                    data.pop(i)
                    write_file(data, source_file)
                    print("Course has been removed successfully")
                else:
                    print("Can't remove course, since students have enrolled in it.")


def update_courses(source_file):
    data = read_file(source_file)
    course_numbers = [course[0] for course in data]
    while True:
        course_number = input("Enter course number: ")
        if course_number in course_numbers:
            break
        else:
            print("Course does not exist")

    choice = input('1. Update course name\n2. Update instructor name\n3. Update section size\nEnter choice: ')

    if choice not in ['1', '2', '3']:
        print("Invalid choice.")
        return
    if choice == '1':
        name = input("Enter name: ")
        for course in data:
            if course_number == course[0]:
                course[3] = name
                print("Course name changed.")
                break
    elif choice == '2':
        instructor = input("Enter instructor name: ")
        for course in data:
            if course_number == course[0]:
                course[-3] = instructor
                print("Instructor name changed.")
                break
    else:
        size = int(input("Enter section size: "))
        for course in data:
            if course_number == course[0]:
                course[-2] = size
                print("Section size changed.")
                break
    write_file(data, source_file)


def register_student(source_file, destination_file):
    data = read_file(source_file)
    course_numbers = [course[0] for course in data]
    while True:
        course_number = input("Enter course number: ")
        if course_number in course_numbers:
            break
        else:
            print("Course number doesn't exist")

    student_id = input("Enter student ID: ")
    student_name = input("Enter student name: ")

    for course in data:
        if course_number == course[0]:
            if int(course[-1]) == int(course[-2]):
                print("Course is full.")
                return
            course[-1] = str(int(course[-1]) + 1)
    write_file(data, source_file)
    try:
        students_details = read_file(destination_file)
        students_details.append([str(course_number), student_name, str(student_id)])
    except:
        students_details = [[str(course_number), student_name, str(student_id)]]
    write_file(students_details, destination_file)
    print("Student registered.")


def drop_student(source_file, destination_file):
    students_details = read_file(destination_file)
    course_number = input("Enter course number: ")
    student_id = input("Enter student ID: ")
    found = False
    for i, student in enumerate(students_details):
        if student_id == student[-1] and course_number == student[0]:
            found = True
            if 'y' == input(f'Enter "y" to confirm removing the student ({student[1]}) from the course ({course_number}): ').lower():
                students_details.pop(i)
                data = read_file(source_file)
                course_name = ""
                for course in data:
                    if course_number == course[0]:
                        course_name = course[3]
                        course[-1] = str(int(course[-1]) - 1)
                        break
                write_file(data, source_file)
                write_file(students_details, destination_file)
                print(f"Student {student_id}, {student[1]} has been dropped from {course_name} successfully")
    if not found:
        print("No student found.")


def main():
    menu = '1. Print courses info\
            \n2. Search for a course\
            \n3. Add new course\
            \n4. Remove a course\
            \n5. Update a course\
            \n6. Register a student in a course\
            \n7. Drop a student from a course\
            \n8. Exit'

    source_file = "coursesInfo.txt"
    destination_file = "registeredStudents.txt"

    while True:
        print("University Registrar System")
        print("=" * 40)
        print(menu)
        print("=" * 40)
        choice = input("Enter your choice: ")

        if choice == '1':
            print_courses_info(source_file)
        elif choice == '2':
            search_course(source_file)
        elif choice == '3':
            add_courses(source_file)
        elif choice == '4':
            remove_courses(source_file)
        elif choice == '5':
            update_courses(source_file)
        elif choice == '6':
            register_student(source_file, destination_file)
        elif choice == '7':
            drop_student(source_file, destination_file)
        else:
            print("GoodBye!")
            break


main()
