from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QLabel, QLineEdit, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from table_model import TableModel
from grading import Grading
from curriculum import Curriculum

from course_registration import Registration


class CurriculumWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Curriculum Report")
        self.setWindowIcon(QIcon("5920.jpg"))
        self.setGeometry(100, 100, 400, 400)
        
        layout = QVBoxLayout(self)

        # create the table view
        self.table = QTableView()
        self.table.setFixedHeight(250)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.program_code_input = QLineEdit()
        self.course_id_input = QLineEdit()

        layout.addWidget(QLabel("Program Code:"))
        layout.addWidget(self.program_code_input)

        #  All courses in a program
        all_courses_in_program_button = QPushButton("Program Curriculum")
        all_courses_in_program_button.clicked.connect(self.all_courses_in_program)
        layout.addWidget(all_courses_in_program_button)

        layout.addWidget(QLabel("Query: "))
        self.query_status = QLabel()
        layout.addWidget(self.query_status)

        # set the table model
        self.model = TableModel([[], []])
    
        self.table.setModel(self.model)

    def all_courses_in_program(self):
        if not self.check_program():
            return
        program_code = self.program_code_input.text()
        
        data_in = Curriculum().report_courses_in_program(program_code)
        cur_id = Curriculum().get_curriculum_id(program_code)
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i]) + [Registration().get_course_name(data_in[i][0])]
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(["Course ID", "Course Name"])
        self.query_status.setText("SELECT curriculum_id FROM program WHERE program_code = {}\n".format(program_code)
        + "SELECT course_id FROM curriculumcourse WHERE curriculum_id = {}".format(cur_id))


    def check_program(self):
        if not self.program_code_input.text():
            self.query_status.setText("Error: program code cannot be empty")
            return False
        
        cur = Curriculum()
        if not cur.check_program(self.program_code_input.text()):
            self.query_status.setText("Error: program code does not exist")
            return False
        return True



if __name__ == "__main__":
    import sys
    parent = None
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CurriculumWindow()
    window.show()
    sys.exit(app.exec_())
