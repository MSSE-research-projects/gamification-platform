from django.test import TestCase

from app.gamification.models import CustomUser


class CustomUserTest(TestCase):

    def test_get_user_full_name(self):
        user = CustomUser(
            andrew_id='user',
            first_name='First',
            last_name='Last',
        )

        full_name = user.get_full_name()

        self.assertEqual(full_name, 'First Last')
