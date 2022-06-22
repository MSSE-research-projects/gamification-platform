from django.test import TestCase

from app.gamification.models import Course, Registration, registration
from app.gamification.models.user import CustomUser


class CourseTest(TestCase):

    def test_get_course(self):
        # Arrange
        course = Course(
            course_name='Course A',
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
            andrew_id='alice',
            email='alice@example.com',
            password='arbitary-password',
        )

        course = Course(
            course_name='Course A',
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
        self.assertEqual(instructors[0].andrew_id, 'alice')
