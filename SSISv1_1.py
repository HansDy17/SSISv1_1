import csv
import hashlib 
import os
from stdiomask import getpass
from cryptography.fernet import Fernet
clear = lambda: os.system('cls')
rec_fields = ['name', 'course', 'id_num', 'age', 'gender', 'email']
student_database = 'students1_1.csv'
pass_db = 'passv1_1.csv'
#course_database = 'course.csv' 

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
    global student_database
    global key
    global fernet

    def add_Student():
        print("---> ADD STUDENT RECORD <---")
        stud_data = []
        for field in rec_fields:
            value = input("Enter " + field + ": ")
            encrypted_value = fernet.encrypt(value.encode()).decode()
            stud_data.append(encrypted_value)

        with open(student_database, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows([stud_data])
        print("---> Data saved successfully! <---")
        
    def show_allStudent(): 
        print("\t\t-----> STUDENTS INFORMATION <-----")
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

    def search_Student(): 
        print("---> SEARCH STUDENT RECORD <---")
        id_num = input("Enter student's ID number to search: ")
        with open(student_database, "r", encoding ="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:                    
                    encrypted_row = row[2]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num == decrypted_row:
                        print("---> STUDENT INFO <---")
                        print("NAME : ", fernet.decrypt(row[0].encode()).decode())
                        print("COURSE : ", fernet.decrypt(row[1].encode()).decode())
                        print("ID NUMBER : ", fernet.decrypt(row[2].encode()).decode())
                        print("AGE : ", fernet.decrypt(row[3].encode()).decode())
                        print("GENDER : ", fernet.decrypt(row[4].encode()).decode())
                        print("EMAIL : ", fernet.decrypt(row[5].encode()).decode())
                        break
            else:
                print("ID Number does not match any student in our Database")

    def update_Student(): 
        print("---> UPDATE STUDENT RECORD <---")
        id_num = input("Input student's ID number to edit: ")
        idx_student = None
        updated_rec = []
        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[2]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num == decrypted_row:
                        idx_student = counter
                        print("Student found at index: ", idx_student)
                        stud_data = []
                        for field in rec_fields:
                            value = input("Input " + field + ": ")
                            stud_data.append(fernet.encrypt(value.encode()).decode())
                        updated_rec.append(stud_data)
                    else:
                        updated_rec.append(row)
                    counter+= 1
        
        if idx_student is not None:
            with open(student_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)
                print("---> Updated successfully! <---")
        else:
            print("ID Number does not match any student in our Database")

    def delete_Student(): 
        print("---> DELETE STUDENT RECORD <---")
        id_num = input("Enter student's ID number to delete: ") 
        stud_locate = False
        updated_rec = []
        with open(student_database, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            counter = 0
            for row in reader:
                if len(row) > 0:
                    encrypted_row = row[2]
                    decrypted_row = fernet.decrypt(encrypted_row.encode()).decode()
                    if id_num != decrypted_row:
                        updated_rec.append(row)
                        counter += 1
                    else:
                        stud_locate = True
        
        if stud_locate is True:
            with open(student_database, "w", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rec)
            print("---> ID number ", id_num, "deleted successfully! <---")
        else: 
            print("ID Number does not match any student in our Database")
    
    def looper(foo):
        clear()
        match foo:
            case 'add': Student.add_Student()
            case 'update': Student.update_Student()
            case 'delete': Student.delete_Student()
            case 'view': Student.search_Student()
            case 'show': Student.show_allStudent()
        itr = True
        while itr:
            if foo == 'show':
                input("Press any key to main menu: ").lower()
                return main()
            ans = input("Press 'y' to " +  foo + " another, any key to main menu: ").lower()
            if ans == 'y':                    
                match foo:
                    case 'add': Student.add_Student()
                    case 'update': Student.update_Student()
                    case 'delete': Student.delete_Student()
                    case 'view': Student.search_Student()
                    case 'show': Student.show_allStudent()
            else:
                itr = False
                main()
            
if __name__ == "__main__":
    
    def main():
        print("===============================================")
        print("-----> SIMPLE STUDENT INFORMATION SYSTEM <-----")
        print("===============================================")
        print("Hi user! What do you want to do?")
        menu = {1: ' ADD STUDENT RECORD',
                2: ' UPDATE STUDENT RECORD',
                3: ' DELETE STUDENT RECORD',
                4: ' VIEW STUDENT RECORD',
                5: ' SHOW RECORD OF STUDENTS',                          
                6: ' Quit'}
        for keys, value in menu.items():
            print("   " + str(keys) + ':' + str(value))
        
        key = input("---> ")
        match key:
            case '1':Student.looper("add")
            case '2':Student.looper("update")
            case '3':Student.looper("delete")
            case '4':Student.looper("view")
            case '5':Student.looper("show")
            case '6':
                    clear()
                    print("Logged out! You're Welcome, goodbye!")
                    quit()

    def login():
        print("Welcome! Please enter username and password to login. \n")
        user1 = ["admin"]
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