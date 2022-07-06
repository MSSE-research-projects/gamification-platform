# import shutil
# import os
from django.test import TestCase
from django.urls import resolve, reverse
# from django.core.files.uploadedfile import SimpleUploadedFile

from app.gamification.forms import AssignmentForm
from app.gamification.views.pages import assignment
from app.gamification.tests.views.pages.utils import LogInUser
from django.conf import settings
from app.gamification.models import Assignment, Course

class AssignmentTest(TestCase):

    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=True)
        
        # create a course first before creating an assignment
        self.course_data = {
            'course_name': 'testName',
            'course_number': '18652',
        }
        self.url = reverse('course')
        self.response = self.client.post(self.url, data=self.course_data)
        
        # get assignment list
        course_id = Course.objects.get(course_name='testName').pk
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        # print(self.url)
        self.response = self.client.get(self.url)
        # print(self.response)
    
    def test_assignment_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_assignment_url_resolves_assignment_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, assignment)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, assignment_name
        '''
        self.assertContains(self.response, 'name="assignment_name"', 1)
    
    def test_add_assignment(self):
        course_id = Course.objects.get(course_name='testName').pk
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.assignment_data = {
            'assignment_name': 'testNameAssignment',
            'course': course_id,
        }
        self.response = self.client.post(self.url, data=self.assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        
    def test_edit_assignment(self):
        # add an assignment first
        course_id = Course.objects.get(course_name='testName').pk
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.assignment_data = {
            'assignment_name': 'testNameAssignment',
            'course': course_id,
        }
        self.response = self.client.post(self.url, data=self.assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        
        # edit the assignment
        assignment_id = Assignment.objects.get(assignment_name = 'testNameAssignment').pk
        self.url = reverse('edit_assignment', kwargs={'course_id': course_id, 'assignment_id': assignment_id})
        self.edit_assignment_data = {
            'course': course_id,
            'assignment_name': 'testNameAssignmentEdited_2',
            'description': 'testDescription',
            'assignment_type': 'Individual',
            'submission_type': 'File',
            'total_score': '100',
            'weight': '100',
            'date_created': '2022-07-06 01:40:03',
            'date_released': '2022-07-06 01:40:03',
            'date_due': '2022-07-06 01:40:03',
            'review_assign_policy': 'A',
        }
        self.response = self.client.post(self.url, data=self.edit_assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited_2').exists())
        
    def test_delete_assignment(self):
        # add an assignment first
        course_id = Course.objects.get(course_name='testName').pk
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.assignment_data = {
            'assignment_name': 'testNameAssignment',
            'course': course_id,
        }
        self.response = self.client.post(self.url, data=self.assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        
        # delete the assignment
        assignment_id = Assignment.objects.get(assignment_name = 'testNameAssignment').pk
        self.url = reverse('delete_assignment', kwargs={'course_id': course_id, 'assignment_id': assignment_id})
        self.response = self.client.delete(self.url)
        # self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
    
        
# class InvalidAssignmentTest(TestCase):
    
    # def setup(self):
    #     test_andrew_id = 'andrew_id'
    #     test_password = '1234'
    #     LogInUser.createAndLogInUser(
    #         self.client, test_andrew_id, test_password, is_superuser=True)
        
    #     # create a course first before creating an assignment
    #     self.course_data = {
    #         'course_name': 'testName',
    #         'course_number': '18652',
    #     }
    #     self.url = reverse('course')
    #     self.response = self.client.post(self.url, data=self.course_data)
        
    #     # TO-DO: course_id might not always be 1
    #     course_id = 1
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     # print(self.url)
    #     self.response = self.client.get(self.url)
    #     # print(self.response)
        
    # def test_add_assignment_invalid(self):
    #     course_id = 1
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': '',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'assignment_name', 'This field is required.')
    
    # def test_add_assignment_invalid_course_id(self):
    #     course_id = -1
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': 'testNameAssignment',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'course_id', 'Invalid course id.')
        
    # def test_add_assignment_invalid_course_id_type(self):
    #     course_id = 'test'
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': 'testNameAssignment',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'course_id', 'Invalid course id.')
        
    # def test_add_assignment_invalid_course_id_none(self):
    #     course_id = None
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': 'testNameAssignment',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'course_id', 'Invalid course id.')
        
    # def test_add_assignment_invalid_course_id_empty(self):
    #     course_id = ''
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': 'testNameAssignment',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'course_id', 'Invalid course id.')
        
    # def test_add_assignment_invalid_course_id_space(self):
    #     course_id = ' '
    #     self.url = reverse('assignment', kwargs={'course_id': course_id})
    #     self.assignment_data = {
    #         'assignment_name': 'testNameAssignment',
    #     }
    #     self.response = self.client.post(self.url, data=self.assignment_data)
    #     self.assertEqual(self.response.status_code, 200)
    #     self.assertFormError(self.response, 'form', 'course_id', 'Invalid course id.')
        
    