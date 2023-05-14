import sys
import datetime
from course_registration import Registration
from grading import Grading
from curriculum import Curriculum
from table_model import TableModel
from report_registration import RegistrationWindow
from report_grading import GradingWindow
from report_curriculum import CurriculumWindow

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QMenu, QAction, QTableView
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("A B Sci Program Application")
        self.setWindowIcon(QIcon('5920.jpg'))
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel("Course Registration System"))
        registration_button = QPushButton("Course Registration")
        registration_button.clicked.connect(self.handle_registration)
        self.layout.addWidget(registration_button)


        registration_report_button = QPushButton("Report Registration")
        registration_report_button.clicked.connect(self.handle_registration_report)
        self.layout.addWidget(registration_report_button)


        self.layout.addWidget(QLabel("Grading System"))
        grading_button = QPushButton("Grade Student")
        grading_button.clicked.connect(self.handle_grading)
        self.layout.addWidget(grading_button)

        receive_grade_button = QPushButton("Receive Grade")
        receive_grade_button.clicked.connect(self.handle_receive_grade)
        self.layout.addWidget(receive_grade_button)

        grade_report_button = QPushButton("Report Grades")
        grade_report_button.clicked.connect(self.handle_grade_report)
        self.layout.addWidget(grade_report_button)


        self.layout.addWidget(QLabel("Curriculum Development System"))
        guidelines_button = QPushButton("Set Curriculum Guidelines")
        guidelines_button.clicked.connect(self.handle_guidelines)
        self.layout.addWidget(guidelines_button)

        curriculum_button = QPushButton("Curriculum Development")
        curriculum_button.clicked.connect(self.handle_curriculum)
        self.layout.addWidget(curriculum_button)

        curriculum_report_button = QPushButton("Report Curriculum")
        curriculum_report_button.clicked.connect(self.handle_curriculum_report)
        self.layout.addWidget(curriculum_report_button)        

        self.layout.addWidget(QLabel("Assignment System"))
        assignment_button = QPushButton("Post Assignment")
        assignment_button.clicked.connect(self.handle_assignment)
        self.layout.addWidget(assignment_button)

        submission_button = QPushButton("Submit Assignment")
        submission_button.clicked.connect(self.handle_submission)
        self.layout.addWidget(submission_button)

        self.layout.setAlignment(Qt.AlignTop)
        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.show()

    def window_setup(self, window, title):
        window.setWindowIcon(QIcon('5920.jpg'))
        window.setWindowTitle(title)
        window.setGeometry(100, 100, 400, 300)

    def handle_registration(self):
        self.registration_window = QMainWindow()
        self.window_setup(self.registration_window, "Course Registration")

        self.student_id_input = QLineEdit()
        self.course_id_input = QLineEdit()

        self.reg_status = QLabel()
        self.del_reg_status = QLabel()

        self.course_name = QLabel()
        self.faculty_member = QLabel()
        self.waitlist_length = QLabel()
        self.course_capacity = QLabel()
        self.available_places = QLabel()

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_student)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_registration)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Student ID:"))
        layout.addWidget(self.student_id_input)
        layout.addWidget(QLabel("Course ID:"))
        layout.addWidget(self.course_id_input)
        layout.addWidget(register_button)
        layout.addWidget(self.reg_status)
        layout.addWidget(delete_button)
        layout.addWidget(self.del_reg_status)

        # Add course information labels
        layout.addWidget(self.course_name)
        layout.addWidget(self.faculty_member)
        layout.addWidget(self.waitlist_length)
        layout.addWidget(self.course_capacity)
        layout.addWidget(self.available_places)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the registration window
        self.registration_window.setCentralWidget(widget)

        # Show the registration window
        self.registration_window.show()

    def register_student(self):
        student_id = self.student_id_input.text()
        course_id = self.course_id_input.text()
        self.reg_status.setText("Course {} does not exist.".format(course_id))
        self.reg_status.setText("Registering student {} for course {}".format(student_id, course_id))
        
        registration = Registration()
        registration.set_registration_input_gui(student_id, course_id)

        if not registration.check_course_availible():  
            self.reg_status.setText("Course {} is not availible. Added to the waitlist".format(course_id))
        elif not registration.check_student_info():
            self.reg_status.setText("Student {} is not eligible.".format(student_id))
        elif registration.check_student_registration():
            self.reg_status.setText("Student {} is already registered for course {}.".format(student_id, course_id))
        else:
            registration.register()
            self.reg_status.setText("Student {} is registered for course {}.".format(student_id, course_id))
        
        self.handle_course_info()

    def delete_registration(self):
        registration = Registration()
        registration.set_registration_input_gui(self.student_id_input.text(), self.course_id_input.text())
        
        if not registration.check_student_info():
            self.del_reg_status.setText("Student {} does not exist".format(self.student_id_input.text()))
        elif not registration.check_student_registration():
            self.del_reg_status.setText("Student {} is not registered for course {}".format(self.student_id_input.text(), self.course_id_input.text()))
        else:
            if len(registration.get_waitlist()) > 0:
                student_id = registration.get_waitlist()[0]
                course_id = registration.get_course_id()
                registration.set_registration_input_gui("Student {} registered for course {}".format(student_id, course_id))
            registration.drop()
            self.del_reg_status.setText("Student {} is deleted from course {}".format(self.student_id_input.text(), self.course_id_input.text()))
        
        self.handle_course_info()

    def handle_course_info(self):
        registration = Registration()
        registration.set_registration_input_gui(self.student_id_input.text(), self.course_id_input.text())
        
        self.course_name.setText("Course name: {}".format(registration.get_course_name(self.course_id_input.text())))
        self.faculty_member.setText("Faculty member: {}".format(registration.get_faculty_member_name()))
        self.available_places.setText("Available places: {}".format(registration.get_availible_places_count()))
        self.course_capacity.setText("Course capacity: {}".format(registration.get_course_capacity()))
        self.waitlist_length.setText("Length of waitlist: {}".format(len(registration.get_waitlist())))
        
    def handle_assignment(self):
        self.assignment_window = QMainWindow()
        self.window_setup(self.assignment_window, "Assignment")

        # Create input fields for faculty member id and course id
        self.faculty_member_id_input = QLineEdit()
        self.course_id_input = QLineEdit()
        self.assignment_type_input = QLineEdit()
        self.assignment_description_input = QLineEdit()
        self.assignment_deadline_input = QLineEdit()
        self.assignment_max_grade_input = QLineEdit()
    
        # Create a button to submit the assignment
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.post_assignment)
        self.submit_status = QLabel()

        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_faculty_member)
        self.sign_in_status = QLabel()

        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # faculty_member_layout = QHBoxLayout()
        layout.addWidget(QLabel("Faculty Member ID:"))
        layout.addWidget(self.faculty_member_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)

        layout.addWidget(QLabel("Course ID:"))
        layout.addWidget(self.course_id_input)
        layout.addWidget(QLabel("Assignment Type:"))
        layout.addWidget(self.assignment_type_input)
        layout.addWidget(QLabel("Assignment Description:"))
        layout.addWidget(self.assignment_description_input)
        layout.addWidget(QLabel("Assignment Deadline:"))
        layout.addWidget(self.assignment_deadline_input)
        layout.addWidget(QLabel("Assignment Max Grade:"))
        layout.addWidget(self.assignment_max_grade_input)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)
        # layout.addWidget(delete_button)

        # # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # # Set the widget as the central widget of the registration window
        self.registration_window.setCentralWidget(widget)

        # Show the registration window
        self.registration_window.show()

    def set_guidance(self, reqcourses_num, program_code, credits=120):
        self.reqcourses_num = reqcourses_num
        self.program_code = program_code
        self.credits = credits
  
    def handle_faculty_member(self):
        #check if faculty member exists
        faculty_member_id = self.faculty_member_id_input.text()
        grading = Grading()
        if grading.check_faculty_member(faculty_member_id):
            self.sign_in_status.setText("Faculty Member {} signed in".format(faculty_member_id))
            return True
        else:
            self.sign_in_status.setText("Faculty Member {} does not exist".format(faculty_member_id))
        return False

    def post_assignment(self):
        if self.handle_faculty_member():
            grading = Grading()
            grading.add_assignment(self.assignment_type_input.text(), self.assignment_description_input.text(),
             self.assignment_deadline_input.text(), self.assignment_max_grade_input.text(),
              self.course_id_input.text())
            self.submit_status.setText("Assignment posted")
        else:
            self.submit_status.setText("Assignment not posted")

    def handle_submission(self):

        # Create a new window for submission
        
        self.submition_window = QMainWindow()
        self.window_setup(self.submition_window, "Submission")

        # Create input fields for student id and course id
        self.student_id_input = QLineEdit()
        self.assignment_id_input = QLineEdit()
        self.submission_file_input = QLineEdit()
        
        # Create a button to submit the assignment
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_assignment)
        self.submit_status = QLabel()

        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_student)
        self.sign_in_status = QLabel()

        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # student_layout = QHBoxLayout()
        layout.addWidget(QLabel("Student ID:"))
        layout.addWidget(self.student_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)

        layout.addWidget(QLabel("Assignment ID:"))
        layout.addWidget(self.assignment_id_input)
        layout.addWidget(QLabel("Submission File:"))
        layout.addWidget(self.submission_file_input)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the registration window
        self.submition_window.setCentralWidget(widget)

        # Show the registration window
        self.submition_window.show()

    def handle_student(self):
        #check if student exists
        student_id = self.student_id_input.text()
        reg  = Registration()
        reg.set_student_id(student_id)
        if reg.check_student_info():
            self.sign_in_status.setText("Student {} signed in".format(student_id))
            return True
        else:
            self.sign_in_status.setText("Student {} not signed in".format(student_id))
            return False
    
    def submit_assignment(self):
        
        grading = Grading()
        if self.handle_student():
            submission_date = datetime.datetime.now().date()
            submission_date_str = submission_date.strftime("%Y-%m-%d")

            grading.add_submission(submission_date_str, self.assignment_id_input.text(), 
            self.submission_file_input.text(), self.student_id_input.text())
            self.submit_status.setText("Assignment submitted")
        else:
            self.submit_status.setText("Assignment not submitted")


    def handle_grading(self):
        # Create a new window for grading
        self.grading_window = QMainWindow()
        self.window_setup(self.grading_window, "Grading")

        # Create input fields for student id and course id
        self.submission_id = QLineEdit()
        self.faculty_member_id_input = QLineEdit()
        self.grade_input = QLineEdit()

        # Create a button to submit the grade
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_grade)
        self.submit_status = QLabel()

        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_faculty_member)
        self.sign_in_status = QLabel()

        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # faculty_member_layout = QHBoxLayout()
        layout.addWidget(QLabel("Faculty Member ID:"))
        layout.addWidget(self.faculty_member_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)

        layout.addWidget(QLabel("Submission ID:"))
        layout.addWidget(self.submission_id)
        layout.addWidget(QLabel("Grade:"))
        layout.addWidget(self.grade_input)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the registration window
        self.grading_window.setCentralWidget(widget)

        # Show the registration window
        self.grading_window.show()

    def submit_grade(self):
        grading = Grading()
        grade = self.grade_input.text()

        grading.set_submission_id(self.submission_id.text())
        grading.set_assignment_id()

        grading.set_grade(grade)

        grade = float(grade)
        max_grade = float(grading.get_max_grade())

        if grade > max_grade:
            self.submit_status.setText("Grade not submitted. Grade exceeds max grade.")
        elif not grading.check_faculty_member(self.faculty_member_id_input.text()):
            self.submit_status.setText("Grade not submitted. Faculty member not signed in.")
        else:
            grading.set_submission_grade()
            self.submit_status.setText("Grade submitted")

    def handle_guidelines(self): 
        self.curriculum = Curriculum()

        # Create a new window for curriculum development
        self.guide_window = QMainWindow()
        self.window_setup(self.guide_window, "Guidelines")

        # Create input fields for course id
        self.administrator_id_input = QLineEdit()
        self.program_code_input = QLineEdit()
        self.cources_num_input = QLineEdit()
        self.credits_input = QLineEdit()

        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_administrator)
        self.sign_in_status = QLabel()

        # Create a button to submit the guidelines
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_guidelines)
        self.submit_status = QLabel()

        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # administrator_layout = QHBoxLayout()
        layout.addWidget(QLabel("Administrator ID:"))
        layout.addWidget(self.administrator_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)

        layout.addWidget(QLabel("Program Code:"))
        layout.addWidget(self.program_code_input)
        layout.addWidget(QLabel("Number of Courses:"))
        layout.addWidget(self.cources_num_input)
        layout.addWidget(QLabel("Credits:"))
        layout.addWidget(self.credits_input)
        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the registration window
        self.guide_window.setCentralWidget(widget)

        # Show the registration window
        self.guide_window.show()

    def submit_guidelines(self):
        if self.handle_administrator():
            self.curriculum.set_guidance(self.cources_num_input.text(), 
            self.program_code_input.text(), self.credits_input.text())
            self.submit_status.setText("Guidelines submitted")
        else:   
            self.submit_status.setText("Guidelines not submitted")

    def handle_administrator(self):
        #check if administrator exists

        administrator_id = self.administrator_id_input.text()
        curriculum = Curriculum()
        if curriculum.check_administrator_info(administrator_id):
            self.sign_in_status.setText("Administrator {} signed in".format(administrator_id))
            return True
        else:
            self.sign_in_status.setText("Administrator {} not signed in".format(administrator_id))
            return False

    def handle_curriculum(self):
        # Create a new window for curriculum development
        self.curriculum_window = QMainWindow()
        self.window_setup(self.curriculum_window, "Curriculum Development")

        # Create input fields for course id
        self.faculty_member_id_input = QLineEdit()
        self.course_id_input = QLineEdit()
        
        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_faculty_member)
        self.sign_in_status = QLabel()

        # Create a button to add course to the curriculum
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        self.add_course_status = QLabel()

        # Create a button to remove course from the curriculum
        remove_course_button = QPushButton("Remove Course")
        remove_course_button.clicked.connect(self.remove_course)
        self.remove_course_status = QLabel()

        # Add submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_curriculum)
        self.submit_status = QLabel()

        self.guidelines_courses_num_status = QLabel()
        self.guidlines_program_code_status = QLabel()
        self.guidelines_credits_status = QLabel()
        self.curriculum_courses_list = QLabel()

        # Add guideline text to QLabel widgets
        self.guidelines_courses_num_status.setText(str(self.curriculum.get_guidance()[0] or 0))
        self.guidlines_program_code_status.setText(str(self.curriculum.get_guidance()[1] or 0))
        self.guidelines_credits_status.setText(str(self.curriculum.get_guidance()[2] or 0))
        self.curriculum_courses_list.setText(str(self.curriculum.get_courses() or 0))


        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # faculty_member_layout = QHBoxLayout()
        layout.addWidget(QLabel("Faculty Member ID:"))
        layout.addWidget(self.faculty_member_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)
        
        layout.addWidget(QLabel("Course ID:"))
        layout.addWidget(self.course_id_input)
        layout.addWidget(add_course_button)
        layout.addWidget(self.add_course_status)
        layout.addWidget(remove_course_button)
        layout.addWidget(self.remove_course_status)

        layout.addWidget(QLabel("Guidelines:"))
        layout.addWidget(QLabel("Number of Courses:"))
        layout.addWidget(self.guidelines_courses_num_status)
        layout.addWidget(QLabel("Program Code:"))
        layout.addWidget(self.guidlines_program_code_status)
        layout.addWidget(QLabel("Credits:"))
        layout.addWidget(self.guidelines_credits_status)
        layout.addWidget(QLabel("Curriculum:"))
        layout.addWidget(self.curriculum_courses_list)

        layout.addWidget(submit_button)
        layout.addWidget(self.submit_status)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the registration window
        self.curriculum_window.setCentralWidget(widget)

        # Show the registration window
        self.curriculum_window.show()
    
    
    def add_course(self):
        if self.handle_faculty_member():
            self.curriculum.add_course(self.course_id_input.text())
            self.add_course_status.setText("Course added")
            self.curriculum_courses_list = self.curriculum.get_courses()
    
    def remove_course(self):
        if self.handle_faculty_member():
            self.curriculum.remove_course(self.course_id_input.text())
            self.remove_course_status.setText("Course removed")
            self.curriculum_courses_list = self.curriculum.get_courses()

    def submit_curriculum(self):
        if not self.handle_faculty_member():
            self.submit_status.setText("Curriculum not submitted")
            print("not faculty member")
        elif not (1 == 1):
            # TODO: Debug
            self.submit_status.setText("Curriculum not submitted")
            print(self.curriculum.reqcourses_num, len(self.curriculum.courses), self.curriculum.courses)
            print("not valid curriculum")
        else:
            self.curriculum.submit_curriculum()
            self.submit_status.setText("Curriculum submitted")


    def handle_receive_grade(self):
        # Create a new window for receiving grades
        self.receive_grade_window = QMainWindow()
        self.window_setup(self.receive_grade_window, "Receive Grade")

        # Create input fields for course id
        self.student_id_input = QLineEdit()
        self.submission_id = QLineEdit()

        # Create Sign In button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.clicked.connect(self.handle_student)
        self.sign_in_status = QLabel()

        # Create a button to add course to the curriculum
        receive_grade_button = QPushButton("Receive Grade")
        receive_grade_button.clicked.connect(self.receive_grade)
        self.receive_grade_status = QLabel()
        self.max_grade_status = QLabel()

        # Add the input fields and register button to a vertical layout
        layout = QVBoxLayout()

        # faculty_member_layout = QHBoxLayout()
        layout.addWidget(QLabel("Student ID:"))
        layout.addWidget(self.student_id_input)
        layout.addWidget(sign_in_button)
        layout.addWidget(self.sign_in_status)
        layout.addWidget(QLabel("Submission ID:"))
        layout.addWidget(self.submission_id)
        layout.addWidget(receive_grade_button)
        layout.addWidget(self.receive_grade_status)
        layout.addWidget(self.max_grade_status)

        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the widget as the central widget of the window
        self.receive_grade_window.setCentralWidget(widget)

        # Show the window
        self.receive_grade_window.show()

    def receive_grade(self):
        grading = Grading()
        grading.set_submission_id(self.submission_id.text())
        grading.set_assignment_id()
        grade = grading.get_submission_grade()
        max_grade = grading.get_max_grade()

        if self.handle_student() and grade:
            self.receive_grade_status.setText("Grade received: " + str(grade))
        else:
            self.receive_grade_status.setText("Grade not received")
        self.max_grade_status.setText("Max grade: " + str(max_grade))

    def handle_grade_report(self):
        grade_report_window = GradingWindow()
        grade_report_window.exec_()

    def handle_curriculum_report(self):
        curriculum_report_window = CurriculumWindow()
        curriculum_report_window.exec_()

    def handle_registration_report(self):
        registration_report_window = RegistrationWindow()
        registration_report_window.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
