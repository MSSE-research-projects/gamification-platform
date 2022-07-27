from django.test import TestCase
from django.urls import resolve, reverse

from app.gamification.models import Course, CustomUser
from app.gamification.models.registration import Registration
from app.gamification.models.survey_template import SurveyTemplate
from app.gamification.serializers import CourseSerializer
from app.gamification.views.api.course import CourseList, CourseDetail


class RetrieveSurveyListTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            andrew_id='testuser',
        )
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='testuser', password='12345')

        self.course = Course(
            course_number='12345',
            course_name='Test Course',
            syllabus='Test Syllabus',
            semester='Fall',
            visible=True,
        )
        self.course.save()

        self.survey = SurveyTemplate(
            name='Test Survey',
            instructions='Test Instructions',
            other_info='Test Other Info',
        )
        self.survey.save()

    def test_student_can_get_all_surveys(self):
        student = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Student,
        )
        student.save()

        self.url = reverse('survey-list')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), list)
        self.assertEqual(len(self.response.json()), 1)
        self.assertEqual(self.response.json()[0]['name'], 'Test Survey')
        self.assertEqual(self.response.json()[
                         0]['instructions'], 'Test Instructions')
        self.assertEqual(self.response.json()[
                         0]['other_info'], 'Test Other Info')


class UpdateSurveyListTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            andrew_id='testuser',
        )
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='testuser', password='12345')

        self.course = Course(
            course_number='12345',
            course_name='Test Course',
            syllabus='Test Syllabus',
            semester='Fall',
            visible=True,
        )
        self.course.save()

        self.url = reverse('survey-list')

    def test_instructor_can_post_survey(self):
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()
        data = {
            'name': 'Test Survey',
            'instructions': 'Test Instructions',
            'other_info': 'Test Other Info',
        }
        self.client.post(self.url, data)
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), list)
        self.assertEqual(len(self.response.json()), 1)
        self.assertEqual(self.response.json()[0]['name'], 'Test Survey')
        self.assertEqual(self.response.json()[
                         0]['instructions'], 'Test Instructions')
        self.assertEqual(self.response.json()[
                         0]['other_info'], 'Test Other Info')

    def test_ta_cannot_post_survey(self):
        ta = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.TA,
        )
        ta.save()
        data = {
            'name': 'Test Survey',
            'instructions': 'Test Instructions',
            'other_info': 'Test Other Info',
        }
        self.client.post(self.url, data)
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), list)
        self.assertEqual(len(self.response.json()), 0)

    def test_instructor_post_a_survey_without_a_name(self):
        ta = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.TA,
        )
        ta.save()
        data = {
            'name': '',
            'instructions': 'Test Instructions',
            'other_info': 'Test Other Info',
        }
        self.client.post(self.url, data)
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), list)
        self.assertEqual(len(self.response.json()), 0)

    def test_instructor_can_post_survey_without_instructions_and_other_info(self):
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()
        data = {
            'name': 'Test Survey',
            'instructions': '',
            'other_info': '',
        }
        self.client.post(self.url, data)
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), list)
        self.assertEqual(len(self.response.json()), 1)
        self.assertEqual(self.response.json()[0]['name'], 'Test Survey')
        self.assertEqual(self.response.json()[
                         0]['instructions'], '')
        self.assertEqual(self.response.json()[
                         0]['other_info'], '')


class RetrieveSurveyDetailTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            andrew_id='testuser',
        )
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='testuser', password='12345')

        self.course = Course(
            course_number='12345',
            course_name='Test Course',
            syllabus='Test Syllabus',
            semester='Fall',
            visible=True,
        )
        self.course.save()

        self.survey = SurveyTemplate(
            name='Test Survey',
            instructions='Test Instructions',
            other_info='Test Other Info',
        )
        self.survey.save()

    def test_student_can_get_survey_detail(self):
        student = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Student,
        )
        student.save()

        self.url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), dict)
        self.assertEqual(self.response.json()['name'], 'Test Survey')
        self.assertEqual(self.response.json()['instructions'],
                         'Test Instructions')
        self.assertEqual(self.response.json()['other_info'], 'Test Other Info')

    def test_instructor_can_get_survey_detail(self):
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()

        self.url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response.json(), dict)
        self.assertEqual(self.response.json()['name'], 'Test Survey')
        self.assertEqual(self.response.json()['instructions'],
                         'Test Instructions')
        self.assertEqual(self.response.json()['other_info'], 'Test Other Info')

    def test_instructor_cannot_get_survey_with_an_invalid_pk(self):
        INVALID_PK = 2
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()

        self.url = reverse(
            'survey-detail', kwargs={'survey_pk': INVALID_PK})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)


class UpdateSurveyDetailTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            andrew_id='testuser',
        )
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='testuser', password='12345')

        self.course = Course(
            course_number='12345',
            course_name='Test Course',
            syllabus='Test Syllabus',
            semester='Fall',
            visible=True,
        )
        self.course.save()

        self.survey = SurveyTemplate(
            name='Test Survey',
            instructions='Test Instructions',
            other_info='Test Other Info',
        )
        self.survey.save()

    def test_instructor_can_update_survey_detail(self):
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()

        url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        data = {
            'name': 'Test Survey 1 ',
            'instructions': 'Test Instructions 1 ',
            'other_info': 'Test Other Info 1',
        }
        self.client.put(url, data, content_type='application/json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()['name'], 'Test Survey 1 ')
        self.assertEqual(response.json()['instructions'],
                         'Test Instructions 1 ')
        self.assertEqual(response.json()[
                         'other_info'], 'Test Other Info 1')

    def test_student_cannot_update_survey_detail(self):
        student = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Student,
        )
        student.save()

        url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        data = {
            'name': 'Test Survey 1 ',
            'instructions': 'Test Instructions 1 ',
            'other_info': 'Test Other Info 1',
        }
        self.client.put(url, data, content_type='application/json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()['name'], 'Test Survey')
        self.assertEqual(response.json()['instructions'],
                         'Test Instructions')
        self.assertEqual(response.json()[
                         'other_info'], 'Test Other Info')

    def test_instructor_can_delete_survey_detail(self):
        instructor = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Instructor,
        )
        instructor.save()

        url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        data = {
            'name': 'Test Survey 1 ',
            'instructions': 'Test Instructions 1 ',
            'other_info': 'Test Other Info 1',
        }
        self.client.delete(url, data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_student_cannot_delete_survey_detail(self):
        student = Registration(
            users=self.user,
            courses=self.course,
            userRole=Registration.UserRole.Student,
        )
        student.save()

        url = reverse(
            'survey-detail', kwargs={'survey_pk': self.survey.id})
        data = {
            'name': 'Test Survey 1 ',
            'instructions': 'Test Instructions 1 ',
            'other_info': 'Test Other Info 1',
        }
        self.client.delete(url, data, content_type='application/json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()['name'], 'Test Survey')
        self.assertEqual(response.json()['instructions'],
                         'Test Instructions')
        self.assertEqual(response.json()[
                         'other_info'], 'Test Other Info')
