import unittest

from curriculum import Curriculum

class TestCurriculum(unittest.TestCase):
    def setUp(self): 
        self.curriculum = Curriculum()
        # reqcourses_num, program_code, credits=120
        self.curriculum.set_guidance(reqcourses_num=5, program_code="CS001", credits=120)
        # faculty_id, faculty_member_id
        self.curriculum.set_faculty(faculty_id=1, faculty_member_id=1)

    def test_get_reqcourses_num(self):
        self.assertEqual(self.curriculum.get_reqcourses_num(), 5)

    def test_get_guidance(self):
        self.assertEqual(self.curriculum.get_guidance(), (5, "CS001", 120))
    
    def test_check_curriculum(self):
        cources_to_add = ['Cybersecurity Fundamentals', 'Discrete Mathematics', 'Probability and Statistics',
        'Cybersecurity Governance']
        for course in cources_to_add:
            self.curriculum.add_course(course)
        self.assertEqual(self.curriculum.check_curriculum(), False)

        self.curriculum.add_course('Data Engineering')
        self.assertEqual(self.curriculum.check_curriculum(), True)
    
    def test_submit_curriculum(self):
        cources_to_add = ['Cybersecurity Fundamentals', 'Discrete Mathematics', 'Probability and Statistics',
        'Cybersecurity Governance', 'Data Engineering']
        for course in cources_to_add:
            self.curriculum.add_course(course)
        print(self.curriculum.get_courses())
        self.assertEqual(self.curriculum.submit_curriculum(), True)


if __name__ == '__main__':
    unittest.main()