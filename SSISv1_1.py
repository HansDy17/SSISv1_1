import csv
import hashlib 
import os
from stdiomask import getpass
from cryptography.fernet import Fernet
clear = lambda: os.system('cls')
rec_fields = ['id_num', 'name', 'gender', 'age', 'course' ,'Year Level',  'email']
course_fields = ['course_code', 'course']
student_database = 'students1_Final.csv'
pass_db = 'passv1_1.csv' # NOT YET USED
course_database = 'course1_Final.csv' 

try:
    with open("keyv1.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("keyv1.key", "wb") as key_file:
        key_file.write(key)
fernet = Fernet(key)

class Student:
    global rec_fields
    global course_fields
    global student_database
    global key
    global fernet

    def add_Student():
        print("---> ADD STUDENT RECORD <---")
        stud_data = []
        course_data = []
        for field in rec_fields:
            value = input("Enter " + field + ": ")
            encrypted_value = fernet.encrypt(value.encode()).decode()
            # if field == "id_num" or field == "course":    
            #     course_data.append(encrypted_value)  
            stud_data.append(encrypted_value)

        with open(student_database, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([stud_data])
        
        # with open(course_database, "a", encoding="utf-8") as f:
        #     writer = csv.writer(f)
        #     writer.writerows([course_data])
        print("---> Data saved successfully! <---")
    
    def add_Course():
        print("---> ADD COURSE RECORD <---")
        #stud_data = []
        course_data = []
        for field in course_fields:
            value = input("Enter " + field + ": ")
            encrypted_value = fernet.encrypt(value.encode()).decode()
            # if field == "id_num" or field == "course":    
            #     course_data.append(encrypted_value)  
            course_data.append(encrypted_value)

        # with open(student_database, "a", encoding="utf-8") as f:
        #     writer = csv.writer(f)
        #     writer.writerows([stud_data])
        
        with open(course_database, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([course_data])
        print("---> Data saved successfully! <---")
        
    def show_allStudent(): 
        print("\t\t\t-----> STUDENTS INFORMATION <-----")
        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for k in rec_fields:                            
                    print('| ' + k, end=' \t ')
            print("\n========================================================================")
            for row in reader:
                for item in row:
                    encrypted_item = item
                    decrypted_item = fernet.decrypt(encrypted_item.encode()).decode()
                    print(' ' + decrypted_item, end='\t |')
                print("\n")

    def show_allCourse(): 
        print("\t-----> LIST OF COURSES <-----")
        with open(course_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for k in course_fields:                            
                    print('| ' + k, end=' \t |')
            print("\n=======================================")
            for row in reader:
                for item in row:
                    encrypted_item = item
                    decrypted_item = fernet.decrypt(encrypted_item.encode()).decode()
                    print(' ' + decrypted_item, end='\t\t |')
                print("\n")    

    def search_Student(): 
        print("---> SEARCH STUDENT RECORD <---")
        id_num = input("Enter student's ID number / Name to search: ")
        with open(student_database, "r", encoding ="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:                    
                    # encrypted_row = row[0], row[1]
                    decrypted_row = fernet.decrypt(row[0].encode()).decode()
                    decrypted_row1 = fernet.decrypt(row[1].encode()).decode()                    
                    if id_num == decrypted_row or id_num.lower() == decrypted_row1.lower():
                        print("---> STUDENT INFO <---")
                        print("ID NUMBER : ", fernet.decrypt(row[0].encode()).decode())
                        print("NAME : ", fernet.decrypt(row[1].encode()).decode())
                        print("GENDER : ", fernet.decrypt(row[2].encode()).decode())
                        print("AGE : ", fernet.decrypt(row[3].encode()).decode())
                        print("COURSE : ", fernet.decrypt(row[4].encode()).decode())
                        print("YEAR LEVEl : ", fernet.decrypt(row[5].encode()).decode())
                        print("EMAIL : ", fernet.decrypt(row[6].encode()).decode())
                        break
            else:
                print("ID Number does not match any student in our Database")

    def search_Course(): 
        print("---> SEARCH COURSE RECORD <---")
        id_num = input("Enter Course Code to search: ")
        with open(course_database, "r", encoding ="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:                    
                    # encrypted_row = row[0], row[1]
                    decrypted_row = fernet.decrypt(row[0].encode()).decode()
                    decrypted_row1 = fernet.decrypt(row[1].encode()).decode()                    
                    if id_num == decrypted_row or id_num.lower() == decrypted_row1.lower():
                        print("---> COURSE INFO <---")
                        print("COURSE CODE : ", fernet.decrypt(row[0].encode()).decode())
                        print("COURSE : ", fernet.decrypt(row[1].encode()).decode())
                        break
            else:
                print("Course Code does not match any course in our Database")

    # def update_Course(id, course_data): 
    #     idx_student = None
    #     course_rec = []
        
    #     with open(course_database, "r", encoding="utf-8") as f:
    #         reader = csv.reader(f)
    #         counter = 0
    #         for row in reader:
    #             if len(row) > 0:
    #                 encrypted_row = row[0]
    #                 decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
    #                 if id == decrypted_row:    
    #                     idx_student = counter                    
    #                     course_rec.append(course_data)
    #                 else:
    #                     course_rec.append(row)                            
    #                 counter+= 1                     
                        
    #     if idx_student is not None:
    #         with open(course_database, "w", encoding="utf-8") as c:
    #             writer1 = csv.writer(c)
    #             writer1.writerows(course_rec)

    def update_Course(): 
        print("---> UPDATE COURSE RECORD <---")
        id_num = input("Input course code to edit: ")
        idx_student = None
        updated_rec = []
        course_data = []      

        with open(course_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num == decrypted_row:
                        idx_student = counter
                        print("Course found at index: ", idx_student)
                        cour_data = []                                          
                        for field in course_fields:
                            value = input("Input " + field + ": ")
                            encrypted_val = fernet.encrypt(value.encode()).decode()
                            cour_data.append(encrypted_val)
                            # if field == "id_num" or field == "course":    
                            #     course_data.append(encrypted_val)               
                            
                        updated_rec.append(cour_data)
                    else:
                        updated_rec.append(row)                            
                    counter+= 1                                  

        if idx_student is not None:
            with open(course_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)

            # Student.update_Course(id_num, course_data)
            # # with open(course_database, "w", encoding="utf-8") as c:
            # #     writer1 = csv.writer(c)
            # #     writer1.writerows(course_rec)
            print("---> Updated successfully! <---")
        else:
            print("ID Number does not match any student in our Database")

    def update_Student(): 
        print("---> UPDATE STUDENT RECORD <---")
        id_num = input("Input student's ID number to edit: ")
        idx_student = None
        updated_rec = []
        course_data = []      

        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num == decrypted_row:
                        idx_student = counter
                        print("Student found at index: ", idx_student)
                        stud_data = []                                          
                        for field in rec_fields:
                            value = input("Input " + field + ": ")
                            encrypted_val = fernet.encrypt(value.encode()).decode()
                            stud_data.append(encrypted_val)
                            # if field == "id_num" or field == "course":    
                            #     course_data.append(encrypted_val)               
                            
                        updated_rec.append(stud_data)
                    else:
                        updated_rec.append(row)                            
                    counter+= 1                                  

        if idx_student is not None:
            with open(student_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)

            # Student.update_Course(id_num, course_data)
            # # with open(course_database, "w", encoding="utf-8") as c:
            # #     writer1 = csv.writer(c)
            # #     writer1.writerows(course_rec)
            print("---> Updated successfully! <---")
        else:
            print("ID Number does not match any student in our Database")

    def delete_Student(): 
        print("---> DELETE STUDENT RECORD <---")
        id_num = input("Enter student's ID number to delete: ") 
        stud_locate = False
        updated_rec = []
        course_rec = []
        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num != decrypted_row:
                        updated_rec.append(row)
                        counter += 1
                    else:
                        stud_locate = True
        
        with open(course_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num != decrypted_row:
                        course_rec.append(row)
                    else:
                        stud_locate = True

        if stud_locate is True:
            with open(student_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)
            with open(course_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(course_rec)
            print("---> ID number ", id_num, "deleted successfully! <---")
        else: 
            print("ID Number does not match any student in our Database")


    def delete_Course(): 
        print("---> DELETE COURSE RECORD <---")
        id_num = input("Enter course code to delete: ") 
        stud_locate = False
        updated_rec = []
        course_rec = []
        with open(course_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num != decrypted_row:
                        updated_rec.append(row)
                        counter += 1
                    else:
                        stud_locate = True
        
        with open(course_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num != decrypted_row:
                        course_rec.append(row)
                    else:
                        stud_locate = True

        if stud_locate is True:
            # with open(student_database, "w", encoding="utf-8") as f:
            #     writer = csv.writer(f)
            #     writer.writerows(updated_rec)
            with open(course_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(course_rec)
            print("---> Course Code deleted successfully! <---")
        else: 
            print("Course code does not match any student in our Database")

# TEST HERE
        idx_student = None
        updated_rec = []
        course_data = []      

        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[0]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num == decrypted_row:
                        idx_student = counter
                        stud_data = []                                          
                        for field in rec_fields:
                            if field == 'course':
                                value = ""
                            encrypted_val = fernet.encrypt(value.encode()).decode()
                            stud_data.append(encrypted_val)
                            
                        updated_rec.append(stud_data)
                    else:
                        updated_rec.append(row)                            
                    counter+= 1                                  

        if idx_student is not None:
            with open(student_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)

    
    def looper(foo):
        clear()
        match foo:
            case 'add': Student.add_Student()
            case 'add_Cour': Student.add_Course()
            case 'update': Student.update_Student()
            case 'update_Cour': Student.update_Course()
            case 'delete': Student.delete_Student()
            case 'delete_Cour': Student.delete_Course()
            case 'search': Student.search_Student()
            case 'search_Cour': Student.search_Course()
            case 'showCourse': Student.show_allCourse()
            case 'showRecord': Student.show_allStudent()
        itr = True
        while itr:
            if foo == 'showCourse' or foo == 'showRecord':
                input("Press any key to main menu: ")
                return main()            
            ans = input("Press 'y' to " +  foo + " another, any key to main menu: ").lower()
            if ans == 'y':                    
                match foo:
                    case 'add': Student.add_Student()
                    case 'add_Cour': Student.add_Course()
                    case 'update': Student.update_Student()
                    case 'update_Cour': Student.update_Course()
                    case 'delete': Student.delete_Student()
                    case 'delete_Cour': Student.delete_Course()
                    case 'search': Student.search_Student()
                    case 'search_Cour': Student.search_Course()
                    case 'showCourse': Student.show_allCourse()
                    case 'showRecord': Student.show_allStudent()
            else:
                itr = False
                main()
            
if __name__ == "__main__":
    
    def main():
        print("===============================================")
        print("-----> SIMPLE STUDENT INFORMATION SYSTEM <-----")
        print("===============================================")
        print("Hi user! What do you want to do?")
        menu = {1: ' ADD STUDENT/COURSE RECORD',
                2: ' UPDATE STUDENT/COURSE RECORD',
                3: ' DELETE STUDENT/COURSE RECORD',
                4: ' SEARCH STUDENT/COURSE RECORD',
                5: ' SHOW LIST OF COURSE',
                6: ' SHOW LIST OF STUDENTS',                          
                7: ' Quit'}
        for keys, value in menu.items():
            print("   " + str(keys) + ':' + str(value))
        
        key = input("---> ")
        match key:
            case '1':
                ask = input("1: Add Student \n2: Add Course\n")
                if ask == '1':
                    Student.looper("add")
                else:
                    Student.looper("add_Cour")
                clear()
            case '2':
                ask = input("1: Update Student \n2: Update Course\n")
                if ask == '1':
                    Student.looper("update")
                else:
                    Student.looper("update_Cour")
                clear()
            case '3':
                ask = input("1: Delete Student \n2: Delete Course\n")
                if ask == '1':
                    Student.looper("delete")
                else:
                    Student.looper("delete_Cour")
                clear()
            case '4':
                ask = input("1: Search Student \n2: Search Course\n")
                if ask == '1':
                    Student.looper("search")
                else:
                    Student.looper("search_Cour")
                clear()
            case '5':
                Student.looper("showCourse")
                clear()
            case '6':
                Student.looper("showRecord")
                clear()
            case '7':
                    clear()
                    print("Logged out! You're Welcome, goodbye!")
                    quit()

    def login():
        print("Welcome! Please enter username and password to login. \n")
        user1 = ["admin", "hans"]
        password1 = hashlib.sha256(str.encode("1234")).hexdigest()
        
        while True:
            userName = input("Enter Your Name: ").lower()
            if userName not in user1:
                print("You Are Not Registered as Admin")
                print()
            else:
                break

        while True:
            userPassword = getpass("Enter Your Password: ")
            if not hashlib.sha256(str.encode(userPassword)).hexdigest() == password1:
                print("Incorrect Password")
                print()
            else:
                break
        print()
        print("Logged In!")
        return True
                            
while True:
    if login():
        main()
