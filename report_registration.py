from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from table_model import TableModel
from grading import Grading
from course_registration import Registration

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__(parent)

        # create the layout
        layout = QVBoxLayout(self)

        # create the table view
        self.table = QTableView()
        layout.addWidget(self.table)

        self.student_id_input = QLineEdit()
        self.assignment_id_input = QLineEdit()
        layout.addWidget(QLabel("Student ID:"))
        layout.addWidget(self.student_id_input)
        layout.addWidget(QLabel("Course ID:"))
        layout.addWidget(self.assignment_id_input)
    
        report_courses_of_student_button = QPushButton("Report Registrations of the Student")
        report_courses_of_student_button.clicked.connect(self.report_courses_of_student)
        layout.addWidget(report_courses_of_student_button)

        report_students_in_course_button = QPushButton("Report Students in the Course")
        report_students_in_course_button.clicked.connect(self.report_students_in_course)
        layout.addWidget(report_students_in_course_button)
        
        report_registrations_button = QPushButton("Report Registrations")
        report_registrations_button.clicked.connect(self.report_registrations)
        layout.addWidget(report_registrations_button)

        # Statistics

        report_num_students_per_course_button = QPushButton("Report Number of Students per Course")
        report_num_students_per_course_button.clicked.connect(self.report_num_students_per_course)
        layout.addWidget(report_num_students_per_course_button)

        report_num_courses_per_student_button = QPushButton("Report Number of Courses per Student")
        report_num_courses_per_student_button.clicked.connect(self.report_num_courses_per_student)
        layout.addWidget(report_num_courses_per_student_button)


        layout.addWidget(QLabel("Query: "))
        self.query_status = QLabel()
        layout.addWidget(self.query_status)

        # set the table model
        self.model = TableModel([[], []])
    
        self.table.setModel(self.model)

    def report_courses_of_student(self):
        student_id = self.student_id_input.text()
        if not student_id:
            self.query_status.setText("Please enter a student ID.")
            return

        data_in = Registration().report_courses_of_student(student_id)
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(header_labels_in=["Course ID"])
        self.query_status.setText("SELECT course_id FROM registration WHERE student_id = {}".format(student_id))

    def report_students_in_course(self):
        course_id = self.assignment_id_input.text()
        if not course_id:
            self.query_status.setText("Please enter a course ID.")
            return

        data_in = Registration().report_students_in_course(course_id)
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(header_labels_in=["Student ID"])
        self.query_status.setText("SELECT student_id FROM registration WHERE course_id = {}".format(course_id))
    
    def report_registrations(self):
        data_in = Registration().report_registrations()
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(header_labels_in=["Course ID", "FacultyMember ID", "Student ID"])
        self.query_status.setText("SELECT * FROM registration")

    def report_num_courses_per_student(self):
        data_in = Registration().report_all_students_statistic()
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(header_labels_in=["Student ID", "Number of Courses"])
        self.query_status.setText("SELECT course_id, COUNT(*) FROM registration GROUP BY course_id")
    
    def report_num_students_per_course(self):
        data_in = Registration().report_all_courses_statistic()
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(header_labels_in=["Course ID", "Number of Students"])
        self.query_status.setText("SELECT student_id, COUNT(*) FROM registration GROUP BY student_id")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    parent = None
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())
