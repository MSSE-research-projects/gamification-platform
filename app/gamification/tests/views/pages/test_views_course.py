from django.test import TestCase
from django.urls import resolve, reverse

from app.gamification.forms import SignUpForm
from app.gamification.models import CustomUser, Course
from app.gamification.views.pages import course
from app.gamification.tests.views.pages.utils import LogInUser 

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
        self.assertEqual(self.response.context.get('registration')[0].courses.course_name, test_course_name)
        self.assertEqual(self.response.context.get('registration')[0].courses.course_number, test_course_number)
        

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
        self.url = reverse('delete_course', args = [1])
        self.client.get(self.url)
        self.assertEqual(0, len(Course.objects.all()))


    def test_delete_course_with_student(self):
        LogInUser.createAndLogInUser(
            self.client, 'user', '123', is_superuser=False)
        self.url = reverse('delete_course', args = [1])
        self.client.get(self.url)
        self.assertEqual(1, len(Course.objects.all()))



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
            'semester':'',
            'syllabus':'',
            'visible':False,
        }
        self.response = self.client.post(self.url, self.data)

    def test_edit_course(self):
        self.data['course_name'] = 'new_course'
        self.data['course_number'] = 456
        self.data['semester'] = '2022FALL'
        self.data['syllabus'] = 'Hello, this is our syllabus'
        self.data['visible'] = True
        self.url = reverse('edit_course', args = [1])
        self.client.post(self.url, self.data)
        course = Course.objects.get(pk = 1)
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
        self.url = reverse('edit_course', args = [1])
        LogInUser.createAndLogInUser(
            self.client, 'user', '123', is_superuser=False)
        self.client.post(self.url, self.data)
        course = Course.objects.get(pk = 1)
        self.assertEqual(course.course_name, 'course1')
        self.assertEqual(course.course_number, '123')
        self.assertEqual(course.semester, '')
        self.assertEqual(course.syllabus, '')
        self.assertEqual(course.visible, False)    


