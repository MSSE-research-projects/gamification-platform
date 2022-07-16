from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from app.gamification.models import CustomUser, Course, Registration
from app.gamification.models.entity import Team
from app.gamification.models.membership import Membership
from app.gamification.tests.views.pages.utils import LogInUser 



class SurveyrTest(TestCase):
    fixtures = ['users.json', 'courses.json', 'registration.json', 'membership.json', 'entities.json', 'assignments.json']

    




