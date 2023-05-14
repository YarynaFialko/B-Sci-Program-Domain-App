import unittest

from course_registration import Registration

class TestCourseRegistration(unittest.TestCase):
    def setUp(self):
        self.course_registration = Registration()
        self.course_registration.set_student_id(1)
        self.course_registration.set_course_name("Cybersecurity Governance")

    
    def test_set_student_id(self):
        self.assertEqual(self.course_registration.get_student_id(), 1)
    
    def test_get_course_id(self):
        self.assertEqual(self.course_registration.get_course_id(), 24)

    def test_request_course_available(self):
        if (self.course_registration.get_availible_places_count()>0):
            self.assertTrue(self.course_registration.check_course_availible())
        else:
            self.assertFalse(self.course_registration.check_course_availible())
    
    # def test_get_availible_places_count(self):
    #     self.assertEqual(self.course_registration.get_availible_places_count(), 10)
    
    def test_get_course(self):
        self.course_registration.set_course_name("Cybersecurity Governance")
        for i in range(11, 20):
            self.course_registration.set_student_id(i)
            self.course_registration.register()
        self.assertFalse(self.course_registration.check_course_availible())
    
    def test_check_student_info(self):
        self.course_registration.set_student_id(1)
        self.assertTrue(self.course_registration.check_student_info())

        self.course_registration.set_student_id(100)
        self.assertFalse(self.course_registration.check_student_info())
    
    def test_waitlist(self):
        self.course_registration.set_course_name("Cybersecurity Governance")
        availible_places = self.course_registration.get_availible_places_count()
        for i in range(0, availible_places+1):
            self.course_registration.set_student_id(i+20)
            self.course_registration.register()
        self.assertEqual(len(self.course_registration.get_waitlist()), 1)


if __name__ == '__main__':
    unittest.main()
