from django.test import TestCase

from app.gamification.models import CustomUser, CustomUserManager


class CustomUserManagerTest(TestCase):

    def setUp(self):
        self.data = {
            'andrew_id': 'alice',
            'email': 'alice@example.com',
            'password': 'arbitary-password',
        }

    def test_create_user(self):
        # Arrange
        manager = CustomUser.objects
        # Act
        manager.create_user(**self.data)
        # Assert
        query_set = CustomUser.objects.filter(andrew_id='alice')
        self.assertTrue(query_set.exists())

    def test_create_superuser(self):
        # Arrange
        manager = CustomUser.objects
        # Act
        user = manager.create_superuser(**self.data)
        # Assert
        query_set = CustomUser.objects.filter(andrew_id='alice')
        self.assertTrue(query_set.exists())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class CustomUserTest(TestCase):

    def test_get_user_full_name(self):
        # Arrange
        user = CustomUser(
            andrew_id='user',
            first_name='First',
            last_name='Last',
        )

        # Act
        full_name = user.get_full_name()

        # Assert
        self.assertEqual(full_name, 'First Last')
