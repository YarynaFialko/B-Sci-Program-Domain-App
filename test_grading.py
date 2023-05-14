import unittest

from grading import Grading

class TestGrading(unittest.TestCase):
    def setUp(self):
        self.grading = Grading()
        self.grading.set_student_id(1)
        self.grading.set_course_id(24)
        # type, description, deadline, max_grade, course_id
        self.grading.add_assignment("Program", "python script", "2023-05-01", 5, 24)
        # submission_date, assignment_id, submission_file, student_id
        self.grading.add_submission("2023-04-01", 1, "file", 1)

        self.grading.set_submission_id(1)
        self.grading.set_assignment_id()

        self.grading.set_grade(2)
        self.grading.set_submission_grade()

    def test_get_max_grade(self):
        self.assertEqual(self.grading.get_max_grade(), 5)

    def test_get_submission_grade(self):
        self.assertEqual(self.grading.get_submission_grade(), 2)
        
        
if __name__ == '__main__':
    unittest.main()
