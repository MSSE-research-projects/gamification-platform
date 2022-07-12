from atexit import register
from urllib import request
from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpResponse

from app.gamification.forms import SignUpForm
from app.gamification.models import CustomUser, Course, Registration
from app.gamification.views.pages import course
from app.gamification.decorators import admin_required, user_role_check
from app.gamification.tests.views.pages.utils import LogInUser
from django.test.client import RequestFactory


class GetCourseTest(TestCase):
    fixtures = ['users.json', 'courses.json', 'registration.json']

    @classmethod
    def setUpTestData(self):
        self.student_andrew_id = 'user1'
        self.student_password = 'user1-password'
        self.ta_andrew_id = 'user4'
        self.ta_password = 'user4-password'
        self.instructor_andrew_id = 'admin1'
        self.instructor_password = 'admin1-password'
        self.admin_andrew_id = 'admin2'
        self.admin_password = 'admin2-password'

        self.invisible_course = Course.objects.get(
            course_number='18749', semester='Summer 2024')
        self.course = Course.objects.get(
            course_number='18652', semester='Fall 2021'
        )

        self.student = CustomUser.objects.get(
            andrew_id=self.student_andrew_id)  # pk = 3
        self.ta = CustomUser.objects.get(andrew_id=self.ta_andrew_id)
        self.instructor = CustomUser.objects.get(
            andrew_id=self.instructor_andrew_id)
        self.admin = CustomUser.objects.get(andrew_id=self.admin_andrew_id)

    def test_get_course(self):
        ENROLLED_COURSE = 1
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('course')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        courses = [
            i.courses.pk for i in self.response.context.get('registration')]
        self.assertIn(ENROLLED_COURSE, courses)

    def test_user_not_in_a_course_view(self):
        NOT_ENROLLED_COURSE = 2
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('course')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        courses = [
            i.courses.pk for i in self.response.context.get('registration')]
        self.assertNotIn(NOT_ENROLLED_COURSE, courses)

    def test_invisible_course_view_for_student(self):
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('course')
        self.response = self.client.get(self.url)
        regis = Registration(
            users=self.student, courses=self.invisible_course)
        regis.save()
        course = [
            i.courses.pk for i in self.response.context.get('registration')]
        self.assertNotIn(4, course)

    def test_invisible_course_view_for_ta(self):
        self.client.login(
            andrew_id=self.ta_andrew_id,
            password=self.ta_password,
        )
        self.url = reverse('course')
        self.response = self.client.get(self.url)
        regis = Registration(
            users=self.ta, courses=self.invisible_course)
        regis.save()
        course = [
            i.courses.pk for i in self.response.context.get('registration')]
        self.assertNotIn(4, course)

    def test_invisible_course_view_for_instructor(self):
        self.client.login(
            andrew_id=self.instructor_andrew_id,
            password=self.instructor_password,
        )
        self.url = reverse('course')
        self.response = self.client.get(self.url)
        regis = Registration(
            users=self.instructor, courses=self.invisible_course)
        regis.save()
        course = [
            i.courses.pk for i in self.response.context.get('registration')]
        self.assertIn(4, course)


class AddCourseTest(TestCase):
    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=True)
        self.url = reverse('course')
        self.response = self.client.get(self.url)

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, course)

    def test_add_course(self):
        test_course_name = "course1"
        test_course_number = "123"
        self.url = reverse('course')
        self.data = {
            'course_name': test_course_name,
            'course_number': test_course_number,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context.get('registration')[
                         0].courses.course_name, test_course_name)
        self.assertEqual(self.response.context.get('registration')[
                         0].courses.course_number, test_course_number)


class InvalidAddCourseTest(TestCase):
    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=True)
        self.url = reverse('course')
        self.response = self.client.get(self.url)

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, course)

    def test_add_course_without_course_name(self):
        test_course_number = "123"
        self.url = reverse('course')
        self.data = {
            'course_number': test_course_number,
        }
        self.response = self.client.post(self.url, self.data)
        form = self.response.context.get('form')
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('course_name', form.errors.keys())

    def test_add_course_without_course_number(self):
        test_course_name = "course1"
        self.url = reverse('course')
        self.data = {
            'course_name': test_course_name,
        }
        self.response = self.client.post(self.url, self.data)
        form = self.response.context.get('form')
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('course_number', form.errors.keys())

    def test_add_course_without_any_input(self):
        self.url = reverse('course')
        self.data = {
        }
        self.response = self.client.post(self.url, self.data)
        form = self.response.context.get('form')
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('course_number', form.errors.keys())
        self.assertIn('course_name', form.errors.keys())


class DeleteCourseTest(TestCase):
    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=True)
        self.url = reverse('course')
        self.client.get(self.url)
        test_course_name = "course1"
        test_course_number = "123"
        self.data = {
            'course_name': test_course_name,
            'course_number': test_course_number,
        }
        self.response = self.client.post(self.url, self.data)

    def test_delete_course(self):
        self.url = reverse('delete_course', args=[1])
        self.client.get(self.url)
        self.assertEqual(0, len(Course.objects.all()))

    def test_delete_course_with_student_or_ta(self):
        LogInUser.createAndLogInUser(
            self.client, 'user', '123', is_superuser=False)
        self.url = reverse('delete_course', args=[1])
        self.client.get(self.url)
        self.assertEqual(1, len(Course.objects.all()))

    def test_delete_non_existing_course(self):
        self.url = reverse('delete_course', args=[5])
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)


class EditCourseTest(TestCase):
    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=True)
        self.url = reverse('course')
        self.client.get(self.url)
        test_course_name = "course1"
        test_course_number = "123"
        self.data = {
            'course_name': test_course_name,
            'course_number': test_course_number,
            'semester': '',
            'syllabus': '',
            'visible': False,
        }
        self.response = self.client.post(self.url, self.data)

    def test_edit_course(self):
        self.data['course_name'] = 'new_course'
        self.data['course_number'] = 456
        self.data['semester'] = '2022FALL'
        self.data['syllabus'] = 'Hello, this is our syllabus'
        self.data['visible'] = True
        self.url = reverse('edit_course', args=[1])
        self.client.post(self.url, self.data)
        course = Course.objects.get(pk=1)
        self.assertEqual(course.course_name, 'new_course')
        self.assertEqual(course.course_number, '456')
        self.assertEqual(course.semester, '2022FALL')
        self.assertEqual(course.syllabus, 'Hello, this is our syllabus')
        self.assertEqual(course.visible, True)

    def test_edit_course_with_student(self):
        self.data['course_name'] = 'new_course'
        self.data['course_number'] = 456
        self.data['semester'] = '2022FALL'
        self.data['syllabus'] = 'Hello, this is our syllabus'
        self.data['visible'] = True
        self.url = reverse('edit_course', args=[1])
        LogInUser.createAndLogInUser(
            self.client, 'user', '123', is_superuser=False)
        self.client.post(self.url, self.data)
        course = Course.objects.get(pk=1)
        self.assertEqual(course.course_name, 'course1')
        self.assertEqual(course.course_number, '123')
        self.assertEqual(course.semester, '')
        self.assertEqual(course.syllabus, '')
        self.assertEqual(course.visible, False)

    def test_edit_non_existing_course(self):
        self.url = reverse('edit_course', args=[5])
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)


class CourseViewTest(TestCase):
    fixtures = ['users.json', 'courses.json', 'registration.json']

    @classmethod
    def setUpTestData(self):
        self.student_andrew_id = 'user1'
        self.student_password = 'user1-password'
        self.ta_andrew_id = 'user4'
        self.ta_password = 'user4-password'
        self.instructor_andrew_id = 'admin1'
        self.instructor_password = 'admin1-password'
        self.admin_andrew_id = 'admin2'
        self.admin_password = 'admin2-password'

        self.course = Course.objects.get(
            course_number='18652', semester='Fall 2021'
        )

        self.student = CustomUser.objects.get(
            andrew_id=self.student_andrew_id)  # pk = 3
        self.ta = CustomUser.objects.get(andrew_id=self.ta_andrew_id)
        self.instructor = CustomUser.objects.get(
            andrew_id=self.instructor_andrew_id)
        self.admin = CustomUser.objects.get(andrew_id=self.admin_andrew_id)

    def test_get_course_info(self):
        EXIST_COURSE = 1
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('view_course', args=[EXIST_COURSE])
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        course = self.response.context.get('course')
        self.assertEqual(course, self.course)

    def test_view_non_existing_course(self):
        NOT_EXIST_COURSE = 100
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('view_course', args=[NOT_EXIST_COURSE])
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)

    def test_view_invisible_course(self):
        INVISIBLE_COURSE = 3
        self.client.login(
            andrew_id=self.student_andrew_id,
            password=self.student_password,
        )
        self.url = reverse('view_course', args=[INVISIBLE_COURSE])
        self.assertRedirects(self.client.get(self.url), reverse('course'))
