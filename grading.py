import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="zireael2020",
  database="hw2"
)

mycursor = mydb.cursor()

class Grading:

    def __init__(self):
        self.student_id = None
        self.course_id = None
        self.submission_id = None
        self.assignment_id = None
        self.grade = None
    
    def set_student_id(self, student_id):
        self.student_id = student_id
    
    def set_course_id(self, course_id):
        self.course_id = course_id
    
    def set_submission_id(self, submission_id):
        self.submission_id = submission_id
    
    def set_grade(self, grade):
        self.grade = grade
    
    def set_assignment_id(self):
        mycursor.execute("SELECT assignment_id FROM submission WHERE submission_id = %s", (self.submission_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Submission id is not valid")
            return False
        else:
            self.assignment_id = myresult[0][0]
            return True

    def get_student_id(self):
        return self.student_id
    
    def get_course_id(self):
        return self.course_id
    
    def get_submission_id(self):
        return self.submission_id

    def get_grade(self):
        return self.grade

    def get_max_grade(self):
        mycursor.execute("SELECT max_grade FROM assignment WHERE assignment_id = %s", (self.assignment_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Assignment id is not valid")
            return False
        else:
            return myresult[0][0]
    
    def get_assignment_id(self):
        return self.assignment_id
    
    # def get_assignment_id_from_submission_id(self):
    #     mycursor.execute("SELECT assignment_id FROM submission WHERE submission_id = %s", (self.submission_id,))
    #     myresult = mycursor.fetchall()
    #     if len(myresult) == 0:
    #         print("Submission id is not valid")
    #         return False
    #     else:
        
    #         return myresult[0][0]

    def check_grade(self):
        return self.grade <= self.get_max_grade()
    
    def check_assignment(self, assignment):
        mycursor.execute("SELECT * FROM assignment WHERE assignment_id = %s", (assignment,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return True
            
    def set_submission_grade(self):
        # if not self.check_grade():
        #     print("Grade is not valid")
        #     return False
        sql = "UPDATE submission SET grade = %s WHERE submission_id = %s"
        val = (self.grade, self.submission_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
    
    def get_submission_grade(self):
        mycursor.execute("SELECT grade FROM submission WHERE submission_id = %s", (self.submission_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Submission id is not valid")
            return False
        else:
            return myresult[0][0]
    
    def check_faculty_member(self, faculty_member_id):
        mycursor.execute("SELECT * FROM facultymember WHERE member_id = %s", (faculty_member_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return True


    def add_assignment(self, task_type, description, deadline, max_grade, course_id):
        # type, description, deadline, max_grade, course_id
        sql = "INSERT INTO assignment (type, description, deadline, max_grade, course_id) VALUES (%s, %s, %s, %s, %s)"
        val = (task_type, description, deadline, max_grade, course_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    
    def add_submission(self, submission_date, assignment_id, submission_file, student_id):
        sql = "INSERT INTO submission (submission_date, submission_file,  assignment_id, grade, student_id) VALUES (%s, %s, %s, %s, %s)"
        val = (submission_date, submission_file, assignment_id, self.grade, student_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    
    def report_mean_grade(self, assignment_id):
        mycursor.execute("SELECT AVG(grade) FROM submission WHERE assignment_id = %s", (assignment_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            return myresult[0][0]
    
    def report_median_grade(self, assignment_id):
        mycursor.execute("SELECT grade FROM submission WHERE assignment_id = %s", (assignment_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            myresult.sort()
            return myresult[len(myresult)//2][0]

    def report_median_for_student(self, student_id):
        mycursor.execute("SELECT grade FROM submission WHERE student_id = %s", (student_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            myresult.sort()
            return myresult[len(myresult)//2][0]

    def report_grades(self, assignment_id):
        mycursor.execute("SELECT grade FROM submission WHERE assignment_id = %s", (assignment_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            return myresult
    
    def report_all_grades_for_assignment(self, assignment_id):
        mycursor.execute("SELECT student_id, grade FROM submission WHERE assignment_id = %s", (assignment_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return myresult
    
    def report_all_grades_for_student(self, student_id):
        mycursor.execute("SELECT assignment_id, grade FROM submission WHERE student_id = %s", (student_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return myresult

    def report_all_grades(self):
        mycursor.execute("SELECT assignment_id, student_id, grade FROM submission")
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return myresult
    
    def report_grades_by_student(self, student_id):
        mycursor.execute("SELECT grade FROM submission WHERE student_id = %s", (student_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            return myresult
    
    def report_mean_for_student(self, student_id):
        mycursor.execute("SELECT AVG(grade) FROM submission WHERE student_id = %s", (student_id,))
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return False
        else:
            return myresult[0][0]


    def report_gpa_for_each_student(self):
        mycursor.execute("SELECT student_id, AVG(grade) FROM submission GROUP BY student_id")
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            print("Course id is not valid")
            return False
        else:
            return myresult

def main():

    grade = Grading()
    # print(grade.check_faculty_member())
    import datetime
    submission_date = datetime.datetime.now().date()
    print(submission_date.strftime("%Y-%m-%d"))
    grade.set_submission_id(13)
    grade.set_assignment_id()
    # print(grade.get_assignment_id_from_submission_id())
    print(grade.get_assignment_id())


    grade.set_grade(2)
    if not grade.check_grade():
        print("here")
        return False
    
    # grade.set_student_id(1)
    # grade.add_assignment("Program", "python script", "2023-05-01", 5, 1)
    # grade.add_submission("2023-04-01", 1, "file", 1)
    # grade.set_submission_id(6)

    # grade.set_grade(2)
    # grade.set_assignment_id()
    # grade.set_submission_grade()
    # print(grade.get_submission_grade())

if __name__ == "__main__":
    main()

