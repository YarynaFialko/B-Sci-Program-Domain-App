import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="*********",
  database="hw2"
)

mycursor = mydb.cursor()

class Curriculum:
  def __init__(self):
    self.courses = []
    self.reqcourses_num = 0
    self.program_code = None
    self.credits = 0
    self.faculty_id = None
    self.faculty_member_id = None
  
  def add_course(self, course):
    self.courses.append(course)
  
  def remove_course(self, course):
    self.courses.remove(course)
  
  def get_courses(self):
    return self.courses

  def get_program_code(self):
    return self.program_code
  
  def get_credits(self):
    return self.credits
  
  def set_credits(self, credits):
    self.credits = credits

  def set_guidance(self, reqcourses_num, program_code, credits=120):
    self.reqcourses_num = reqcourses_num
    self.program_code = program_code
    self.credits = credits
  
  def set_faculty(self, faculty_id, faculty_member_id):
    self.faculty_id = faculty_id
    self.faculty_member_id = faculty_member_id

  def get_reqcourses_num(self):
    return self.reqcourses_num

  def get_guidance(self):
    return self.reqcourses_num, self.program_code, self.credits

  def check_course_exists(self, course):
    mycursor.execute("SELECT course_name FROM course")
    myresult = mycursor.fetchall()
    for x in myresult:
      if x[0] == course:
        return True
    return False

  def get_existing_courses(self, show=True):
    mycursor.execute("SELECT * FROM course")
    myresult = mycursor.fetchall()
    if show:
      for x in myresult:
        print(x)
    return myresult

  def add_course_to_db(self, course):
    sql = "INSERT INTO course (course_name, faculty_id, faculty_member_id ) VALUES (%s, %s, %s)"
    val = (course, self.faculty_id, self.faculty_member_id)
    mycursor.execute(sql, val)
    mydb.commit()
  
  def delete_course_from_db(self, course):
    sql = "DELETE FROM course WHERE course_name = %s"
    val = (course,)
    mycursor.execute(sql, val)
    mydb.commit()

  def update_course(self, course, new_course):
    sql = "UPDATE course SET course_name = %s WHERE course_name = %s"
    val = (new_course, course)
    mycursor.execute(sql, val)
    mydb.commit()
  
  def get_course_id(self, course):
    mycursor.execute("SELECT course_id FROM course where course_name = %s", (course,))
    myresult = mycursor.fetchall()
    return myresult[0][0]

  def check_curriculum(self):
    return len(self.courses) == self.reqcourses_num
  
  def add_courses(self, courses):
    for course in courses:
      self.add_course(course)

  def add_administrator(self, administration_id, person_id):
    sql = "INSERT INTO administrator (administration_id, person_id) VALUES (%s, %s)"
    val = (administration_id, person_id)
    mycursor.execute(sql, val)
    mydb.commit()

  
  def load_courses_db(self):
    if self.check_curriculum():
      for course in self.courses:
        if not self.check_course_exists(course):
          self.add_course_to_db(course=course)
      print("Your curriculum has been submitted successfully.")
    else:
      if len(self.courses) > self.reqcourses_num:
        print("You have added too many courses to your curriculum. Please remove some courses and try again.")
      else: 
        print("You have not added enough courses to your curriculum. Please add more courses and try again.")
  

  def add_curriculum_to_bd(self):
    sql = "INSERT INTO curriculum (credits) VALUES (%s)"
    val = (self.credits,)
    mycursor.execute(sql, val) 
    mydb.commit()

  def assign_curriculum_to_program(self, curriculum_id):
    sql = "UPDATE program SET curriculum_id = %s WHERE program_code = %s"
    val = (curriculum_id, self.program_code)
    mycursor.execute(sql, val)
    mydb.commit()

  def fill_curriculum_with_courses(self, curriculum_id):
    for course in self.courses:
      course_id = self.get_course_id(course)
      sql = "INSERT INTO curriculumcourse (curriculum_id, course_id) VALUES (%s, %s)"
      val = (curriculum_id, course_id)
      mycursor.execute(sql, val)
      mydb.commit()


  def submit_curriculum(self):
    if not self.check_curriculum():
      print("You have not added enough courses to your curriculum. Please add more courses and try again.")
      return False

    # add curriculum to curriculum table
    self.add_curriculum_to_bd()

    # get the curriculum id
    mycursor.execute("SELECT curriculum_id FROM curriculum WHERE credits = %s", (self.credits,))
    myresult = mycursor.fetchall()
    curriculum_id = myresult[0][0]

    # add all courses to course table
    self.load_courses_db()

    # curriculumcourse table (curriculum_id, course_id)
    self.fill_curriculum_with_courses(curriculum_id)
    
    # assign to the program table attribute curriculum_id
    self.assign_curriculum_to_program(curriculum_id)

    return True

  def check_administrator_info(self, admin_id):
    mycursor.execute("SELECT * FROM administrator where administrator_id = %s", (admin_id,))
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
      return False
    return True

  def delete_curriculum(self):
    mycursor.execute("DELETE FROM curriculum WHERE program_code = %s", (self.program_code,))
    mydb.commit()
    print("Your curriculum has been deleted successfully.")

  def update_guidance(self):
    print("Please enter the number of required courses for this curriculum.")
    reqcourses_num = input()
    self.set_guidance(reqcourses_num, self.program_code)
    print("Your guidance has been updated successfully.")
  
  def report_courses_in_curriculum(self, curriculum_id):
    sql = "SELECT course_id FROM curriculumcourse WHERE curriculum_id = %s"
    val = (curriculum_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

  def get_curriculum_id(self, program_code):
    sql = "SELECT curriculum_id FROM program WHERE program_code = %s"
    val = (program_code,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult[0][0]
  
  def report_courses_in_program(self, program_code):
    curriculum_id = self.get_curriculum_id(program_code)
    return self.report_courses_in_curriculum(curriculum_id)

  def report_curriculums_numcourses(self):
    sql = "SELECT curriculum_id, COUNT(*) FROM curriculumcourse GROUP BY curriculum_id"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult
  
  def report_course_numcurriculums(self):
    sql = "SELECT course_id, COUNT(*) FROM curriculumcourse GROUP BY course_id"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult
  

  def check_program(self, program_code):
    mycursor.execute("SELECT * FROM program where program_code = %s", (program_code,))
    myresult = mycursor.fetchall()
    if len(myresult) == 0:
      return False
    return True
  
  def get_course_name_from_id(self, course_id):
    mycursor.execute("SELECT course_name FROM course where course_id = %s", (course_id,))
    myresult = mycursor.fetchall()
    return myresult[0][0]

def faculty_sign_in(curr):
  print("Please enter your faculty ID.")
  faculty_id = input()
  print("Please enter your faculty member ID.")
  faculty_member_id = input()
  sql = "SELECT * FROM facultymember WHERE faculty_id = %s AND member_id = %s"
  val = (faculty_id, faculty_member_id)
  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()
  if len(myresult) > 0:
    curr.set_faculty(faculty_id, faculty_member_id)
    return True
  else:
    return False

def faculty_role(curr):
  print("Welcome to the Curriculum Development system.")
  if faculty_sign_in(curr):
    #guidance  notice
    print("The quidance courses number is: " + curr.get_reqcourses_num())
    print("The program code is: " + curr.get_program_code())
    print(curr.get_courses())
    print(len(curr.get_courses()))
    print()
 
    #add courses
    print("Please enter the courses (course_name) you would like to add from the curriculum.")
    print("Please enter 'done' when you are finished.")
    course = None
    while course != "done":
      course = input()
      if course != "done" or course != None:
        curr.add_course(course)
    
    print("Your course has been added successfully.")

    #remove courses
    print("Please enter the courses (course_name) you would like to remove from the curriculum.")
    print("Please enter 'done' when you are finished.")
    course = None
    while course != "done":
      course = input()
      if course != "done" or course != None:
        curr.remove_course(course)
    print("Your course has been removed successfully.")

    admin_role_review(curr)
  else:
    print("Invalid faculty ID or faculty member ID. Please try again.")
    faculty_role(curr)


def admin_sign_in():
  print("Please enter your admin ID.")
  admin_id = input()
  print("Please enter your admin member ID.")
  admin_member_id = input()
  sql = "SELECT * FROM admin_member WHERE admin_id = %s AND admin_member_id = %s"
  val = (admin_id, admin_member_id)
  mycursor.execute(sql, val)
  myresult = mycursor.fetchall()
  if len(myresult) > 0:
    return True
  else:
    return False

def admin_role_guidance(curr):
  # if admin_sign_in():
  if True:
    #set guidance
    print("Please enter the program code.")
    program_code = input()
    print("Please enter the guidance courses number.")
    reqcourses_num = input()
    print("Please enter the credits for this curriculum.")
    credits = input()
    curr.set_guidance(reqcourses_num, program_code, credits)
    print("Your guidance courses number has been set successfully.")
    print("Your program code has been set successfully.")
    faculty_role(curr)

def admin_role_review(curr):
  if curr.check_curriculum():
    # add to the database
    curr.submit_curriculum()
    print("Your curriculum has been submitted successfully.")
  else:
    print("Your curriculum has not been submitted successfully.")
    curr.update_guidance()
    faculty_role(curr)
    
def main():

  curr = Curriculum()
  # curr.set_guidance(1, "CS001", 3)
  # curr.add_administrator(1, 15)
  # curr.add_administrator(2, 16)
  # curr.add_administrator(3, 17)

  # print(curr.get_guidance()[0] or 0)

  # print(curr.report_courses_in_program(program_code="CS001"))
  print(curr.check_program(1))
  

  #Clear curriculumcourse table
  # mycursor.execute("DELETE FROM curriculumcourse")
  # mydb.commit()

  # curr = Curriculum()
  # curr.set_guidance(1, "CS001")

  # curr.add_course("WevDev")

  # curr.submit_curriculum()
  # print("DONE")

  # print(curr.check_curriculum())
if __name__ == "__main__":
  main()
