from django.test import TestCase
from django.urls import resolve, reverse

from app.gamification.forms import SignUpForm
from app.gamification.models import CustomUser, Course, Registration
from app.gamification.views.pages import course
from app.gamification.tests.views.pages.utils import LogInUser 

class AddMemberTest(TestCase):
    def setUp(self):
        LogInUser.createAndLogInUser(
            self.client, 'exist_id', '123', is_superuser=False)
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
        self.course_pk = self.response.context.get('courses')[0].pk

    def test_add_member(self):
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = 'exist_id'
        test_member_team = 'T1'
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context.get('membership')[0][0], test_member_andrewId)
        self.assertEqual(self.response.context.get('membership')[0][1], test_member_role)
        self.assertEqual(self.response.context.get('membership')[0][2], test_member_team)
    
    def test_add_inexistent_member(self):
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = 'not_exist_id'
        test_member_team = 'T1'
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context.get('membership'), [])
    
    def test_add_member_without_team(self):
        #andrewID, Role, Team
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = 'exist_id'
        test_member_team = ''
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.context.get('membership')[0][0], test_member_andrewId)
        self.assertEqual(self.response.context.get('membership')[0][1], test_member_role)
        self.assertEqual(self.response.context.get('membership')[0][2], test_member_team)

    def test_add_team_without_andrewId(self):
        #andrewID, Role, Team
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = ''
        test_member_team = 'T1'
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertEqual(self.response.status_code, 200)
        self.assertIn('Andrew Id', self.response.context.get('membership').errors.keys())

    def test_add_member_not_superuser(self):
        test_andrew_id = 'andrew_id_1'
        test_password = '12345'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=False)
            
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = 'Andrew_id'
        test_member_team = 'T1'
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.response = self.client.post(self.url, self.data)
        self.assertRedirects(self.response, reverse('course'))


class DeleteMemberTest(TestCase):
    def setUp(self):
        LogInUser.createAndLogInUser(
            self.client, 'exist_id', '123', is_superuser=False)
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
        self.course_pk = self.response.context.get('courses')[0].pk
        self.url = reverse('member_list', args = [self.course_pk])
        test_member_andrewId = 'exist_id'
        test_member_team = 'T1'
        test_member_role = 'Student'
        self.data = {
            'andrew_id': test_member_andrewId,
            'team_name': test_member_team,
            'membershipRadios': test_member_role,
        }
        self.client.post(self.url, self.data)

    def test_delete_member(self):
        self.url = reverse('delete_member', args = [self.course_pk, 'exist_id'])
        self.client.get(self.url)
        registratiton = Registration.objects.all()
        self.assertEqual(0, len(registratiton))
    
    def test_delete_member_not_superuser(self):
        test_andrew_id = 'andrew_id_1'
        test_password = '12345'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password, is_superuser=False)
        self.url = reverse('delete_member', args = [self.course_pk, 'exist_id'])
        self.client.get(self.url)
        registratiton = Registration.objects.all()
        self.assertEqual(1, len(registratiton))
        