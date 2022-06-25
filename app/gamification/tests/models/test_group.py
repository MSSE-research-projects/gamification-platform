from contextlib import nullcontext
from tokenize import group
from unicodedata import name
from django.test import TestCase

from app.gamification.models import Group, Individual, Team


class GroupTest(TestCase):
    def test_get_team_from_group(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()
        team_group_pk = team.group_ptr_id

        # Act
        group = Group.objects.get(pk=team_group_pk)

        # Assert
        self.assertEqual(group.team.name, 'team1')
        self.assertEqual(group.team.id, team.id)

    def test_get_individual_from_group(self):
        # Arrange
        individual = Individual()
        individual.save()
        individual_group_pk = individual.group_ptr_id

        # Act
        group = Group.objects.get(pk=individual_group_pk)

        # Assert
        self.assertEqual(group.individual.id, individual.id)

    def test_get_error_from_group_without_individual(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()
        team_group_pk = team.group_ptr_id

        individual = Individual()
        individual.save()

        # Act
        group = Group.objects.get(pk=team_group_pk)

        # Assert
        with self.assertRaises(Exception):
            group.individual

    def test_get_error_from_group_without_team(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()

        individual = Individual()
        individual.save()
        individual_group_pk = individual.group_ptr_id

        # Act
        group = Group.objects.get(pk=individual_group_pk)

        # Assert
        with self.assertRaises(Exception):
            group.team
