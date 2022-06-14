from django.test import TestCase

from app.gamification.models import CustomUser


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
