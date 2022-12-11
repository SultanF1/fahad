def read_file(inFileName):
    listOfCourses = []
    with open(inFileName) as file:
        for line in file.readlines():
            line = line.strip().split(',')
            listOfCourses.append(line)
    return listOfCourses


def write_file(data, outFileName):
    with open(outFileName, "w") as file:
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


def print_courses_info(inFileName):
    data = read_file(inFileName)
    print_headers()
    for course in data:
        print_course_details(course)


def search_course(inFileName):
    data = read_file(inFileName)
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
        courseNumber = input("Enter course number: ").lower()
        print_headers()
        for course in data:
            if courseNumber == course[0].lower():
                found = True
                print_course_details(course)

    if not found:
        print("No course found.")


def add_courses(inFileName):
    data = read_file(inFileName)
    courseNumbers = [course[0] for course in data]
    course = []
    courseNumber = input("Enter course number: ")
    if (not courseNumber.isnumeric()) or (len(courseNumber) != 5) or (courseNumber in courseNumbers):
        print("Invalid input.")
        return
    course.append(courseNumber)
    courseCode = input("Enter course code: ")
    if len(courseCode) == 0:
        print("Invalid input.")
        return
    course.append(courseCode)
    section = input("Enter section number: ")
    if int(section) < 1:
        print("Invalid input.")
        return
    course.append(section)
    courseName = input("Enter course name: ")
    if len(courseName) == 0:
        print("Invalid input.")
        return
    course.append(courseName)
    instructor = input("Enter instructor name: ")
    if len(instructor) == 0:
        print("Invalid input.")
        return
    course.append(instructor)
    size = str(input("Enter section size: "))
    if int(size) < 1:
        print("Invalid input.")
        return
    course.append(size)
    course.append('0')
    data.append(course)
    write_file(data, inFileName)
    print("Course added.")


def remove_courses(inFileName):
    data = read_file(inFileName)
    courseNumbers = [course[0] for course in data]
    while True:
        courseNumber = input("Enter course number: ")
        if not (courseNumber in courseNumbers):
            print("Invalid input.")
        else:
            break
    print_headers()
    for i, course in enumerate(data):
        if courseNumber == course[0]:
            print_course_details(course)
            if 'y' == input("Enter 'y' to confirm removing: ").lower():
                if int(course[-1]) == 0:
                    data.pop(i)
                    write_file(data, inFileName)
                else:
                    print("Can't remove course, since students have enrolled in it.")


def update_courses(inFileName):
    data = read_file(inFileName)
    courseNumbers = [course[0] for course in data]
    while True:
        courseNumber = input("Enter course number: ")
        if not (courseNumber in courseNumbers):
            print("Invalid input.")
        else:
            break
    choice = input('1. Update course name\n2. Update instructor name\n3. Update section size\nEnter choice: ')
    if choice not in ['1', '2', '3']:
        print("Invalid choice.")
        return
    if choice == '1':
        name = input("Enter name: ")
        for course in data:
            if courseNumber == course[0]:
                course[3] = name
                print("Course name changed.")
                break
    elif choice == '2':
        instructor = input("Enter instructor name: ")
        for course in data:
            if courseNumber == course[0]:
                course[-3] = instructor
                print("Instructor name changed.")
                break
    else:
        size = int(input("Enter section size: "))
        for course in data:
            if courseNumber == course[0]:
                course[-2] = size
                print("Section size changed.")
                break
    write_file(data, inFileName)


def register_student(inFileName, outFileName):
    data = read_file(inFileName)
    courseNumbers = [course[0] for course in data]
    while True:
        courseNumber = input("Enter course number: ")
        if not (courseNumber in courseNumbers):
            print("Invalid input.")
        else:
            break
    studentID = input("Enter student ID: ")
    studentName = input("Enter student name: ")
    for course in data:
        if courseNumber == course[0]:
            if int(course[-1]) == int(course[-2]):
                print("Course is full.")
                return
            course[-1] = str(int(course[-1]) + 1)
    write_file(data, inFileName)
    try:
        studentsDetails = read_file(outFileName)
        studentsDetails.append([str(courseNumber), studentName, str(studentID)])
    except:
        studentsDetails = [[str(courseNumber), studentName, str(studentID)]]
    write_file(studentsDetails, outFileName)
    print("Student registered.")


def drop_student(inFileName, outFileName):
    studentsDetails = read_file(outFileName)
    courseNumber = input("Enter course number: ")
    studentID = input("Enter student ID: ")
    found = False
    for i, student in enumerate(studentsDetails):
        if studentID == student[-1] and courseNumber == student[0]:
            found = True
            print(student)
            if 'y' == input("Enter 'y' to confirm removing: ").lower():
                studentsDetails.pop(i)
                data = read_file(inFileName)
                for course in data:
                    if courseNumber == course[0]:
                        course[-1] = str(int(course[-1]) - 1)
                        break
                write_file(data, inFileName)
                write_file(studentsDetails, outFileName)
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
    print("University Registrar System")
    while True:
        inFileName = "coursesInfo.txt"
        outFileName = "registeredStudents.txt"
        print("=" * 40)
        print(menu)
        print("=" * 40)
        while True:
            choice = input("Enter your choice: ")
            if choice not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                print("Invalid choice. Try again.")
            else:
                break
        if choice == '1':
            print_courses_info(inFileName)
        elif choice == '2':
            search_course(inFileName)
        elif choice == '3':
            add_courses(inFileName)
        elif choice == '4':
            remove_courses(inFileName)
        elif choice == '5':
            update_courses(inFileName)
        elif choice == '6':
            register_student(inFileName, outFileName)
        elif choice == '7':
            drop_student(inFileName, outFileName)
        else:
            print("GoodBye!")
            break


main()