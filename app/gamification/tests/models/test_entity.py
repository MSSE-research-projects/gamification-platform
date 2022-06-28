from django.test import TestCase

from app.gamification.models import Entity, Individual, Team, CustomUser, Course, Membership, Registration


class EntityTest(TestCase):
    def test_get_team_from_entity(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()
        team_entity_pk = team.entity_ptr_id

        # Act
        entity = Entity.objects.get(pk=team_entity_pk)

        # Assert
        self.assertEqual(entity.team.name, 'team1')
        self.assertEqual(entity.team.id, team.id)

    def test_get_individual_from_entity(self):
        # Arrange
        individual = Individual()
        individual.save()
        individual_entity_pk = individual.entity_ptr_id

        # Act
        entity = Entity.objects.get(pk=individual_entity_pk)

        # Assert
        self.assertEqual(entity.individual.id, individual.id)

    def test_get_error_from_entity_without_individual(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()
        team_entity_pk = team.entity_ptr_id

        individual = Individual()
        individual.save()

        # Act
        entity = Entity.objects.get(pk=team_entity_pk)

        # Assert
        with self.assertRaises(Exception):
            entity.individual

    def test_get_error_from_entity_without_team(self):
        # Arrange
        team = Team(
            name='team1'
        )
        team.save()

        individual = Individual()
        individual.save()
        individual_entity_pk = individual.entity_ptr_id

        # Act
        entity = Entity.objects.get(pk=individual_entity_pk)

        # Assert
        with self.assertRaises(Exception):
            entity.team

    def test_get_member(self):
        # Arrange
        individual = Individual()
        individual.save()
        individual_entity_pk = individual.entity_ptr_id
        entity = Entity.objects.get(pk=individual_entity_pk)

        user = CustomUser.objects.create_user(
            andrew_id='test3',
            email='test3@example.com',
            password='arbitary-password',
        )

        course = Course(
            course_name='Course C',
            course_number='888',
            syllabus='Syllabus',
            semester='Semester',
        )
        course.save()

        registration = Registration(
            users=user,
            courses=course,
            userRole=Registration.UserRole.TA,
        )
        registration.save()

        membership = Membership(
            student=registration,
            entity=entity,
        )
        membership.save()
        # Act
        members = entity.members

        # Assert
        self.assertEqual(len(members), 1)
        self.assertEqual(members[0].andrew_id, 'test3')
