from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableView, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from table_model import TableModel
from grading import Grading
from curriculum import Curriculum

from course_registration import Registration


class CurriculumWindow(QDialog):
    def __init__(self):

        super().__init__(parent)

        # create the layout
        layout = QVBoxLayout(self)

        # create the table view
        self.table = QTableView()
        layout.addWidget(self.table)

        self.program_code_input = QLineEdit()
        self.course_id_input = QLineEdit()

        layout.addWidget(QLabel("Program Code:"))
        layout.addWidget(self.program_code_input)
        # layout.addWidget(QLabel("Course ID:"))
        # layout.addWidget(self.course_id_input)

        
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
        print("all_courses_in_program")
        program_code = self.program_code_input.text()

        if program_code == "":
            self.query_status.setText("Error: program code cannot be empty")
            return
        
        data_in = Curriculum().report_courses_in_program(program_code)
        for i in range(len(data_in)):
            data_in[i] = list(data_in[i])
        self.model.updateData(data_in)
        self.model.updateHeaderLabels(["Course ID"])
        self.query_status.setText("SELECT curriculum_id from program WHERE program_code = {}".format(program_code))

if __name__ == "__main__":
    import sys
    parent = None
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CurriculumWindow()
    window.show()
    sys.exit(app.exec_())
