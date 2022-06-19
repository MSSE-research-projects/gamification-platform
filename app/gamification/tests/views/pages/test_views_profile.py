import shutil
import os
from django.test import TestCase
from django.urls import resolve, reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from app.gamification.forms import ProfileForm
# FIX: Remove unnecessary imports and comments
from app.gamification.models import CustomUser
from app.gamification.views.pages import profile
from app.gamification.tests.views.pages.utils import LogInUser
# NOTE: This is the right way of dynamically importing settings
# (Remove this note before making next commit)
from django.conf import settings


class ProfileTest(TestCase):

    def setUp(self):
        test_andrew_id = 'andrew_id'
        test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, test_andrew_id, test_password)
        self.url = reverse('profile')
        self.response = self.client.get(self.url)

    def test_profile_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_profile_url_resolves_profile_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, profile)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ProfileForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, andrew_id, email, first_name, last_name, image
        FIX: Four inputs? Why no assertion on the number of '<input' elements?
        '''
        self.assertContains(self.response, 'name="email"', 1)
        self.assertContains(self.response, 'name="first_name"', 1)
        self.assertContains(self.response, 'name="last_name"', 1)
        self.assertContains(self.response, 'name="image"', 1)


class SuccessfulEditProfileTest(TestCase):

    def setUp(self):
        if(os.path.exists(settings.MEDIA_ROOT)):
            shutil.rmtree(settings.MEDIA_ROOT)

        self.test_andrew_id = 'andrew_id'
        self.test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, self.test_andrew_id, self.test_password)

        # NOTE: If you don't understand what these lines are doing,
        # PLEASE GO SEARCH AND FIGURE IT OUT!!!
        filepath = settings.STATICFILES_DIRS[0] / 'images/faces/face1.jpg'
        f = open(filepath, 'rb')
        uploaded_image = SimpleUploadedFile(
            name=filepath,
            content=f.read(),
            content_type='image/jpg'
        )
        self.data = {
            'email': 'alice@example.com',
            'first_name': 'Alex',
            'last_name': 'He',
            'image': uploaded_image
        }

        self.url = reverse('profile')
        self.response = self.client.post(self.url, data=self.data)

    def tearDown(self):
        # Remove MEDIA directory after tests finish
        if(os.path.exists(settings.MEDIA_ROOT)):
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_user_info_updated(self):
        # Arrange
        response = self.client.get(self.url)
        # Act
        user = response.context.get('user')
        # Assert
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(user.andrew_id, self.test_andrew_id)
        self.assertEqual(user.email, 'alice@example.com')
        self.assertEqual(user.first_name, 'Alex')
        self.assertEqual(user.last_name, 'He')
        self.assertEqual(
            str(settings.MEDIA_ROOT / 'profile_pics/face1.jpg'),  user.image.path)


class InvalidEditProfileTest(TestCase):

    def setUp(self):
        self.test_andrew_id = 'andrew_id'
        self.test_password = '1234'
        LogInUser.createAndLogInUser(
            self.client, self.test_andrew_id, self.test_password)
        self.url = reverse('profile')

        # FIX: Rewrite the dict into a cleaner way
        # Refere to `SuccessfulEditProfileTest.setUp` for reference
        self.data = {
            'email': 'alice@example.com',
            'first_name': 'Tom',
            'last_name': 'James',
            'image': SimpleUploadedFile('face1.jpg',
                                        content=open(settings.STATICFILES_DIRS[0] / 'images/faces/face1.jpg', 'rb').read(), content_type='image/jpg'),

        }
        # self.response = self.client.post(self.url, self.data)

    # FIX: Are these next 4 tests considered **invalid**?
    def test_edit_profile_with_no_email(self):
        # Arrange
        self.data['email'] = ''
        # Act
        response = self.client.post(self.url, self.data)
        user = response.context.get('user')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.email, '')

    def test_edit_profile_with_no_firstname(self):
        # Arrange
        self.data['first_name'] = ''
        # Act
        response = self.client.post(self.url, self.data)
        user = response.context.get('user')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, '')

    def test_edit_profile_with_no_lastname(self):
        # Arrange
        self.data['last_name'] = ''
        # Act
        response = self.client.post(self.url, self.data)
        user = response.context.get('user')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.last_name, '')

    def test_edit_profile_with_no_image(self):
        # Arrange
        self.data['image'] = ''
        # Act
        response = self.client.post(self.url, self.data)
        user = response.context.get('user')
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.image, '')

    def test_edit_profile_with_anonymous_user(self):
        # Arrange
        self.client.logout  # FIX: Why didn't call this function?
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        # TODO: logout and edit profile should return 401 Unauthorized or assertRedirects
        # FIX: Make assertions on what it is supposed to do.
        # - Return 401 status code
        # - Redirect to signin page
        self.assertEqual(response.status_code, 200)

    # FIX: Rename 'wrong image' to 'invalid type of file'
    def test_edit_profile_with_wrong_image(self):
        # Arrange
        self.data['image'] = SimpleUploadedFile('face1.pdf',
                                                content=open(settings.STATICFILES_DIRS[0] / 'images/faces/face1.pdf', 'rb').read(), content_type='image/jpg'),
        # Act
        response = self.client.post(self.url, self.data)
        # Assert
        # TODO: Unprocessable Entity or assertRedirects or err msg
        self.assertEqual(response.status_code, 200)
        # FIX: Isn't it supposed to give some error message in the form, like
        # the SignUpForm. Make those assertions here.
