import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="zireael2020",
  database="hw2"
)

mycursor = mydb.cursor()

class Registration:

    def __init__(self):
        self.student_id = None
        self.course_name = None
        self.waitlist = []
        self.availible = False

    def set_student_id(self, student_id):
        self.student_id = student_id
    
    def set_course_name(self, course_name):
        self.course_name = course_name

    def get_student_id(self):
        return self.student_id
    
    def get_course_name(self):
        return self.course_name

    def get_course_name(self, course_id):
        sql = "SELECT course_name FROM course WHERE course_id = %s"
        val = (course_id,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult[0][0]

    def set_registration_input(self, student_id, course_name):
        self.set_student_id(student_id)
        self.set_course_name(course_name)

    def set_registration_input_gui(self, student_id, course_id ):
        self.set_registration_input(student_id, self.get_course_name(course_id))

    def get_course_id(self):
        mycursor.execute("SELECT course_id FROM course WHERE course_name = %s", (self.course_name,))
        myresult = mycursor.fetchall()
        return myresult[0][0]
    
    def get_faculty_member_id(self):
        mycursor.execute("SELECT faculty_member_id FROM course WHERE course_name = %s", (self.course_name,))
        myresult = mycursor.fetchall()
        return myresult[0][0]
    
    def get_faculty_member_name(self):
        id = self.get_faculty_member_id()
        mycursor.execute("SELECT person_id FROM facultymember WHERE member_id = %s", (id,))
        myresult = mycursor.fetchall()
        id = myresult[0][0]
        mycursor.execute("SELECT first_name, last_name FROM person WHERE person_id = %s", (id,))
        myresult = mycursor.fetchall()
        return myresult[0][0] + " " + myresult[0][1]

    def set_availible(self):
        self.availible = True

    def get_course_capacity(self):
        mycursor.execute("SELECT capacity FROM course WHERE course_name = %s", (self.course_name,))
        myresult = mycursor.fetchall()
        return myresult[0][0]
        
    def check_course_availible(self):
        if self.get_availible_places_count() > 0:
            self.set_availible()
            return True
        return False
    
    def get_availible_places_count(self):
        mycursor.execute("SELECT course_id, capacity FROM course WHERE course_name = %s", (self.course_name,))
        myresult = mycursor.fetchall()
        capacity = myresult[0][1]
        course_id = myresult[0][0]
        if len(myresult) != 0:
            sql = "SELECT COUNT(*) FROM registration WHERE course_id = %s"
            val = (course_id,)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            registered = myresult[0][0]
            return capacity - registered
        return False

    def update_registrations(self):
        sql = "UPDATE registration SET faculty_member_id = %s WHERE course_id = %s"
        val = (self.get_faculty_member_id(), self.get_course_id(self.course_name))
        mycursor.execute(sql, val)
        mydb.commit()
        return True

    def check_student_info(self):
        mycursor.execute("SELECT * FROM student WHERE student_id = %s", (self.student_id,))
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            return True
        return False
    
    def check_student_registration(self):
        mycursor.execute("SELECT * FROM registration WHERE student_id = %s AND course_id = %s", (self.student_id, self.get_course_id()))
        myresult = mycursor.fetchall()
        if len(myresult) != 0:
            return True
        return False


    def register(self):
        if self.check_course_availible() and self.check_student_info() and not self.check_student_registration():
            course_id = self.get_course_id()
            faculty_member_id = self.get_faculty_member_id()
            sql = "INSERT INTO registration (course_id, faculty_member_id, student_id) VALUES (%s, %s, %s)"
            val = (course_id, faculty_member_id,self.student_id)
            mycursor.execute(sql, val)
            mydb.commit()
            self.send_confirmation()
            return True
        self.send_denial()
        if not self.check_student_registration():
            self.add_to_waitlist() 
            self.send_add_to_waitlist()   
        return False

    def add_to_waitlist(self):
        if self.check_student_info():
            self.waitlist.append(self.student_id)
    
    def drop(self):
        if self.check_student_info():
            sql = "DELETE FROM registration WHERE student_id = %s AND course_id = %s"
            val = (self.student_id, self.get_course_id())
            mycursor.execute(sql, val)
            mydb.commit()
            self.manage_waitlist()
            return True
        return False

    def drop_from_waitlist(self):
        if self.check_student_info():
            self.waitlist.remove(self.student_id)
    
    def get_waitlist(self):
        return self.waitlist
    
    def manage_waitlist(self):
        if self.check_course_availible():
            if len(self.waitlist) != 0:
                self.student_id = self.waitlist.pop(0)
                self.register()
                return True
        return False
    
    def send_confirmation(self):
        print("Registration confirmed!")
    
    def send_denial(self):
        print("Registration denied!")

    def send_add_to_waitlist(self):
        print("Added to waitlist!") 

    def report_student_registrations(self):
        # return all courses registered by a student
        mycursor.execute("SELECT * FROM registration WHERE student_id = %s", (self.student_id,))
        myresult = mycursor.fetchall()
        return myresult
    
    def report_courses_of_student(self, student):
        # return all courses registered by a student
        mycursor.execute("SELECT course_id FROM registration WHERE student_id = %s", (student,))
        myresult = mycursor.fetchall()
        return myresult

    def report_students_in_course(self, course_id):
        # return all students registered in a course
        mycursor.execute("SELECT student_id FROM registration WHERE course_id = %s", (course_id,))
        myresult = mycursor.fetchall()
        return myresult

    def report_course_registrations(self):
        # return all students registered in a course
        mycursor.execute("SELECT * FROM registration WHERE course_id = %s", (self.get_course_id(),))
        myresult = mycursor.fetchall()
        return myresult
    
    def report_all_courses_statistic(self):
        # return all courses and the number of students registered in each course
        mycursor.execute("SELECT course_id, COUNT(*) FROM registration GROUP BY course_id")
        myresult = mycursor.fetchall()
        return myresult
    
    def report_all_students_statistic(self):
        # return all students and the number of courses registered by each student
        mycursor.execute("SELECT student_id, COUNT(*) FROM registration GROUP BY student_id")
        myresult = mycursor.fetchall()
        return myresult
    
    def report_registrations(self):
        # return all registrations
        mycursor.execute("SELECT * FROM registration")
        myresult = mycursor.fetchall()
        return myresult

    def report_course_waitlist(self):
        return self.waitlist
    
    


def main():
    reg = Registration()

    print(reg.get_course_name(1))
    reg.set_registration_input_gui(15, 1)
    print(reg.get_faculty_member_name())


    # reg.set_student_id(1)
    # reg.set_course_name("Data Engineering")
    # reg.register()

    # print(reg.report_course_registrations())




if __name__ == "__main__":
    main()