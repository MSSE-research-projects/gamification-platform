from django.test import TestCase
from django.urls import resolve, reverse

from django.contrib.auth.forms import AuthenticationForm
from app.gamification.models import CustomUser
from app.gamification.views.pages import signin


class SignUpTest(TestCase):

    def setUp(self):
        self.url = reverse('signin')
        self.response = self.client.get(self.url)

    def test_signin_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signin_url_resolves_signin_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, signin)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)

    def test_form_inputs(self):

        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'name="username"', 1)
        self.assertContains(self.response, 'name="password"', 1)



class SuccessfulSignInTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(andrew_id='jiad')
        user.set_password('yunshan123')
        user.save()
        self.url = reverse('signin')
        self.data = {
            'username': 'jiad',
            'password': 'yunshan123',
        }
        self.response = self.client.post(self.url, self.data)
        self.profile_url = reverse('profile')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to profile page
        '''
        self.assertRedirects(self.response, self.profile_url)



    def test_user_authentication(self):


        # Arrange
        response = self.client.get(self.profile_url)
        # Act
        user = response.context.get('user')
        # Assert
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.andrew_id, 'jiad')


class InvalidSignInTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(andrew_id='jiad')
        user.set_password('yunshan123')
        user.save()
        self.url = reverse('signin')
        self.profile_url = reverse('profile')
        self.data = {
            'username': 'yunshan123',
            'password': '123',
        }


    def test_signin_with_wrong_password(self):
        response = self.client.post(self.url, self.data)
        # Assert
        self.assertEqual(response.status_code, 200)

