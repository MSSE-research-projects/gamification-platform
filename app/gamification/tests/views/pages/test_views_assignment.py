from django.test import TestCase
from django.urls import resolve, reverse

from app.gamification.forms import AssignmentForm
from app.gamification.views.pages import assignment
from app.gamification.tests.views.pages.utils import LogInUser
from django.conf import settings
from app.gamification.models import Assignment, Course

# TO-DO test with a user that is not an instructor
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
            'assignment_name': 'testNameAssignmentEdited',
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
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
        
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
        self.assertEqual(self.response.status_code, 302) # TO-DO: 302?
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
    
        
class InvalidAssignmentTest(TestCase):
    
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
        self.response = self.client.get(self.url)
        
    def test_get_assignment_with_invalid_course_id(self):
        course_id = Course.objects.get(course_name='testName').pk
        course_id += 1 # invalid course id
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)
        
    def test_add_assignment_without_assignment_name(self):
        course_id = Course.objects.get(course_name='testName').pk
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.assignment_data = {
            'assignment_name': '',
            'course': course_id,
        }
        self.response = self.client.post(self.url, data=self.assignment_data)
        self.assertEqual(self.response.status_code, 200)
        # TO-DO: return error message when assignment name is empty
        # self.assertFormError(self.response, 'form', 'assignment_name', 'This field is required.')
    
    def test_add_assignment_invalid_course_id(self):
        course_id = Course.objects.get(course_name='testName').pk
        course_id += 1 # invalid course id
        self.url = reverse('assignment', kwargs={'course_id': course_id})
        self.assignment_data = {
            'assignment_name': 'testNameAssignment',
        }
        self.response = self.client.post(self.url, data=self.assignment_data)
        self.assertEqual(self.response.status_code, 404)
    
    def test_edit_assignment_with_invalid_date_format(self):
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
            'assignment_name': 'testNameAssignmentEdited',
            'description': 'testDescription',
            'assignment_type': 'Individual',
            'submission_type': 'File',
            'total_score': '100',
            'weight': '100',
            'date_created': '202', # invalid date
            'date_released': '2022-07-06 01:40:03',
            'date_due': '2022-07-06 01:40:03',
            'review_assign_policy': 'A',
        }
        self.response = self.client.post(self.url, data=self.edit_assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
    
    def test_edit_assignment_with_invalid_date_format_2(self):
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
            'assignment_name': 'testNameAssignmentEdited',
            'description': 'testDescription',
            'assignment_type': 'Individual',
            'submission_type': 'File',
            'total_score': '100',
            'weight': '100',
            'date_created': '2022-07-06 01:40:03',
            'date_released': '202', # invalid date
            'date_due': '2022-07-06 01:40:03',
            'review_assign_policy': 'A',
        }
        self.response = self.client.post(self.url, data=self.edit_assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
        
    def test_edit_assignment_with_invalid_date_format_3(self):
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
            'assignment_name': 'testNameAssignmentEdited',
            'description': 'testDescription',
            'assignment_type': 'Individual',
            'submission_type': 'File',
            'total_score': '100',
            'weight': '100',
            'date_created': '2022-07-06 01:40:03',
            'date_released': '2022-07-06 01:40:03',
            'date_due': '202', # invalid date
            'review_assign_policy':'A',
        }
        self.response = self.client.post(self.url, data=self.edit_assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
    
    def test_edit_assignment_with_invalid_assignment_type(self):
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
            'assignment_name': 'testNameAssignmentEdited',
            'description': 'testDescription',
            'assignment_type': 'InvalidInputTest',
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
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
        
    def test_edit_assignment_with_invalid_submission_type(self):
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
            'assignment_name': 'testNameAssignmentEdited',
            'description': 'testDescription',
            'assignment_type': 'Individual',
            'submission_type': 'InvalidInputTest', # invalid submission type
            'total_score': '100',
            'weight': '100',
            'date_created': '2022-07-06 01:40:03',
            'date_released': '2022-07-06 01:40:03',
            'date_due': '2022-07-06 01:40:03',
            'review_assign_policy': 'A',
        }
        self.response = self.client.post(self.url, data=self.edit_assignment_data)
        self.assertEqual(self.response.status_code, 200)
        self.assertFalse(Assignment.objects.filter(assignment_name = 'testNameAssignmentEdited').exists())
    
    def test_delete_assignment_not_exist(self):
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
        
        # delete the assignment (assignment does not exist)
        assignment_id = Assignment.objects.get(assignment_name = 'testNameAssignment').pk
        assignment_id += 1 # invalid assignment id
        self.url = reverse('delete_assignment', kwargs={'course_id': course_id, 'assignment_id': assignment_id})
        self.response = self.client.delete(self.url)
        self.assertEqual(self.response.status_code, 404)
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        
    def test_delete_assignment_invalid_course_id(self):
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
        assignment_id += 1 # invalid assignment id
        self.url = reverse('delete_assignment', kwargs={'course_id': course_id, 'assignment_id': assignment_id})
        self.response = self.client.delete(self.url)
        self.assertEqual(self.response.status_code, 404) 
        self.assertTrue(Assignment.objects.filter(assignment_name = 'testNameAssignment').exists())
        
        
    