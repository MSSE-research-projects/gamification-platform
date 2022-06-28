from django.test import TestCase

from app.gamification.models import Course, Registration, registration
from app.gamification.models.user import CustomUser


class CourseTest(TestCase):

    def test_get_course(self):
        # Arrange
        course = Course(
            course_name='Course A',
            course_number='888',
            syllabus='Syllabus',
            semester='Semester',
        )

        # Act
        course_name = course.get_course_name()

        # Assert
        self.assertEqual(course_name, 'Course A')

    def test_get_Instructor(self):
        # Arrange
        user = CustomUser.objects.create_user(
            andrew_id='test1',
            email='test1@example.com',
            password='arbitary-password',
        )

        course = Course(
            course_name='Course A',
            course_number='888',
            syllabus='Syllabus',
            semester='Semester',
        )
        course.save()

        registration = Registration(
            users=user,
            courses=course,
            userRole=Registration.UserRole.Instructor,
        )
        registration.save()

        # Act
        instructors = course.instructors

        # Assert
        self.assertEqual(len(instructors), 1)
        self.assertEqual(instructors[0].andrew_id, 'test1')

    def test_get_Student(self):
        # Arrange
        user = CustomUser.objects.create_user(
            andrew_id='test2',
            email='test2@example.com',
            password='arbitary-password',
        )

        course = Course(
            course_name='Course B',
            course_number='888',
            syllabus='Syllabus',
            semester='Semester',
        )
        course.save()

        registration = Registration(
            users=user,
            courses=course,
            userRole=Registration.UserRole.Student,
        )
        registration.save()

        # Act
        students = course.students

        # Assert
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].andrew_id, 'test2')

    def test_get_TA(self):
        # Arrange
        user = CustomUser.objects.create_user(
            andrew_id='test3',
            email='test3@example.com',
            password='arbitary-password',
        )

        course = Course(
            course_name='Course C',
            course_number='888',
            syllabus='Syllabus',
            semester='Semester',
        )
        course.save()

        registration = Registration(
            users=user,
            courses=course,
            userRole=Registration.UserRole.TA,
        )
        registration.save()

        # Act
        TAs = course.TAs

        # Assert
        self.assertEqual(len(TAs), 1)
        self.assertEqual(TAs[0].andrew_id, 'test3')
