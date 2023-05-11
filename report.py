from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from table_model import TableModel
from grading import Grading
from course_registration import Registration

class MyNewWindow(QDialog):
    def __init__(self, parent=None):
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
        layout.addWidget(QLabel("Assignment ID:"))
        layout.addWidget(self.assignment_id_input)

        # Create a report mean for assignment button 
        report_mean_button = QPushButton("Report Mean for Assignment")
        report_mean_button.clicked.connect(self.report_mean_for_assignment)
        self.report_mean_for_assignment_status = QLabel()
        layout.addWidget(report_mean_button)
        layout.addWidget(self.report_mean_for_assignment_status)


        # Create a report mean for student button
        report_mean_for_student_button = QPushButton("Report Mean for Student")
        report_mean_for_student_button.clicked.connect(self.report_mean_for_student)
        self.report_mean_for_student_status = QLabel()
        layout.addWidget(report_mean_for_student_button)
        layout.addWidget(self.report_mean_for_student_status)

        # Report all grades for assignment button
        report_all_grades_for_assignment_button = QPushButton("Report All Grades for Assignment")
        report_all_grades_for_assignment_button.clicked.connect(self.report_all_grades_for_assignment)
        layout.addWidget(report_all_grades_for_assignment_button)

        # Report all grades for student button
        report_all_grades_for_student_button = QPushButton("Report All Grades for Student")
        report_all_grades_for_student_button.clicked.connect(self.report_all_grades_for_student)
        layout.addWidget(report_all_grades_for_student_button)

        # Report all grades button
        report_all_grades_button = QPushButton("Report All Grades")
        report_all_grades_button.clicked.connect(self.report_all_grades)
        layout.addWidget(report_all_grades_button)

        layout.addWidget(QLabel("Query: "))
        self.query_status = QLabel()
        layout.addWidget(self.query_status)


        # set the table model
        self.model = TableModel([[], []])
    
        self.table.setModel(self.model)

        self.grading = Grading()
        

    def report_mean_for_assignment(self):
        mean = Grading().report_mean_grade(self.assignment_id_input.text())
        self.report_mean_for_assignment_status.setText("Mean for the assignment: " + str(mean))
        self.query_status.setText("SELECT AVG(grade) FROM submission WHERE assignment_id = {}".format(self.assignment_id_input.text()))

    def report_mean_for_student(self):
        mean = self.grading.report_mean_for_student(self.student_id_input.text())
        self.report_mean_for_student_status.setText("Mean for student: " + str(mean))
        self.query_status.setText("SELECT AVG(grade) FROM submission WHERE student_id = {}".format(self.student_id_input.text()))

    
    def report_all_grades_for_assignment(self):
        if not self.check_assignment():
            return
        data_in = self.grading.report_all_grades_for_assignment(self.assignment_id_input.text())
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(["Student ID", "Grade"])
        self.query_status.setText("SELECT student_id, grade FROM submission WHERE assignment_id = {}".format(self.assignment_id_input.text()))

    def report_all_grades_for_student(self):
        if not self.check_student():
            return
        data_in = self.grading.report_all_grades_for_student(self.student_id_input.text())
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(["Assignment ID", "Grade"])
        self.query_status.setText("SELECT assignment_id, grade FROM submission WHERE student_id = {}".format(self.student_id_input.text()))


    def report_all_grades(self):
        data_in = self.grading.report_all_grades()
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(["Student ID", "Assignment ID", "Grade"])
        self.query_status.setText("SELECT assignment_id, student_id, grade FROM submission")


    def check_student(self):
        regisstration = Registration()
        regisstration.set_student_id(self.student_id_input.text())
        if not regisstration.check_student() and not None:
            selt.query_status.setText("Student ID does not exist")
            return False
        return True

    def check_assignment(self):
        regisstration = Registration()
        regisstration.set_assignment_id(self.assignment_id_input.text())
        if not regisstration.check_assignment() and not None:
            selt.query_status.setText("Assignment ID does not exist")
            return False
        return True

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MyNewWindow()
    # name the window
    window.setWindowTitle("Report Grades")
    window.show()
    sys.exit(app.exec_())
