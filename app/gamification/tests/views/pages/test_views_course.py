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
        self.assertEqual(self.response.context.get('courses')[0].course_name, test_course_name)
        self.assertEqual(self.response.context.get('courses')[0].course_number, test_course_number)
        

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
        self.assertEqual(self.response.status_code, 200)
        #TODO: return an error message when empty course_number
        self.assertIn('name', self.response.context.get('courses').errors.keys())

    def test_add_course_without_course_number(self):
        test_course_name = "course1"
        self.url = reverse('course')
        self.data = {
            'course_name': test_course_name,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        #TODO: return an error message when empty course_name
        self.assertIn('number', self.response.context.get('courses').errors.keys())

    def test_add_course_without_any_input(self):
        self.url = reverse('course')
        self.data = {
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        #TODO: return an error message when empty course_name and course_number
        self.assertIn('number', self.response.context.get('courses').errors.keys())



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

        