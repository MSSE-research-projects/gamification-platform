from app.gamification import models

from .publisher import Subscriber, register_subscriber


@register_subscriber()
class Registration(Subscriber):

    def create(self, obj, *args, **kwargs):
        if obj is None:
            users = kwargs.get('users')
            courses = kwargs.get('courses')
            userRole = kwargs.get('userRole')
            obj, _ = models.Registration.objects.get_or_create(
                users=users, courses=courses, userRole=userRole
            )

        if obj.userRole == 'Student':
            # Create an individual entity for the student if there are individual assignments
            INDIVIDUAL = models.Assignment.AssigmentType.Individual
            if obj.courses.assignments.filter(assignmentType=INDIVIDUAL).exists():
                # Check if an individual entity already exists for the student
                # FIX: 'registration=obj' may not work in filter
                if not models.Individual.objects.filter(course=obj.courses, registration=obj).exists():
                    entity = self.publisher.notify(
                        Individual, 'create', course=courses)
                # Check if the student is already a member of the entity
                if not models.Membership.objects.filter(student=obj, entity=entity).exists():
                    self.publisher.notify(
                        Membership, 'create', student=obj, entity=entity)

        return obj

    def update(self, obj, *args, **kwargs):
        if obj is None:
            raise ValueError('Registration object is None')

        new_users = kwargs.get('users', obj.users)
        new_courses = kwargs.get('courses', obj.courses)
        new_userRole = kwargs.get('userRole', obj.userRole)

        if new_users != obj.users or new_courses != obj.courses:
            # Delete old registration
            self.publisher.notify(Registration, 'delete', obj=obj)
            # Create new registration
            self.publisher.notify(
                Registration, 'create',
                users=new_users, courses=new_courses, userRole=new_userRole)

        if new_userRole != obj.userRole:
            # If userRole is from STUDENT to INSTRUCTOR/TA, delete old registration
            if new_userRole in ['Instructor', 'TA'] and obj.userRole in ['Student']:
                self.publisher.notify(
                    Registration, 'delete', obj=obj, commit=False)
            # If new userRole is from INSTRUCTOR/TA to STUDENT, create new registration
            if new_userRole == 'Student' and obj.userRole in ['Instructor', 'TA']:
                obj.userRole = new_userRole
                obj.save()
                self.publisher.notify(Registration, 'create', obj=obj)

    def delete(self, obj, commit=True):
        # Delete related membership objects
        for membership in models.Membership.objects.filter(student=obj):
            self.publisher.notify(Membership, 'delete', obj=membership)

        if commit:
            obj.delete()


@register_subscriber()
class Entity(Subscriber):
    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        # Delete all its memberships
        for membership in models.Membership.objects.filter(entity=obj):
            self.publisher.notify(Membership, 'delete', obj=membership)

        # No need to call `obj.delete` here because the entity has been
        # automatically deleted in `Membership.delete` when the last member
        # is removed.


@register_subscriber()
class Individual(Entity):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            course = kwargs.get('course')
            obj, _ = models.Individual.objects.get_or_create(course=course)

        return obj


@register_subscriber()
class Team(Entity):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            course = kwargs.get('course')
            name = kwargs.get('name')
            obj, _ = models.Team.objects.get_or_create(
                course=course, name=name)

        return obj


@register_subscriber()
class Membership(Subscriber):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            student = kwargs.get('student')
            entity = kwargs.get('entity')
            obj, _ = models.Membership.objects.get_or_create(
                student=student, entity=entity)

        # Create ArtifactReview for the student
        # Notify each artifact for all assignments in the course
        for assignment in models.Assignment.objects.filter(course=student.courses):
            for artifact in models.Artifact.objects.filter(entity__not=entity, assignment=assignment):
                self.publisher.notify(Artifact, 'create_review', obj=artifact)

        return obj

    def update(self, obj, *args, **kwargs):
        if obj is None:
            raise ValueError('Membership object is None')

        new_entity = kwargs.get('entity', obj.entity)
        new_student = kwargs.get('student', obj.student)
        if new_entity != obj.entity or new_student != obj.student:
            # Delete the old membership
            self.publisher.notify(Membership, 'delete', obj=obj)
            # Create the new membership
            self.publisher.notify(Membership, 'create',
                                  student=new_student, entity=new_entity)

    def delete(self, obj: models.Membership):
        # Delete related ArtifactReview
        reg = obj.student
        for artifact_review in models.ArtifactReview.filter(user=reg):
            self.publisher.notify(
                ArtifactReview, 'delete', obj=artifact_review)

        entity = obj.entity
        obj.delete()

        # Delete the entity if last member is deleted
        #
        # NOTE:
        # The entity is deleted here when the last member is deleted,
        # so no need to call `obj.delete` in `Entity.delete`.
        if len(entity.members) == 0:
            entity.delete()


@register_subscriber()
class Course(Subscriber):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            course_number = kwargs.get('course_number')
            course_name = kwargs.get('course_name')
            syllabus = kwargs.get('syllabus')
            semester = kwargs.get('semester')
            visible = kwargs.get('visible')
            obj, _ = models.Course.objects.get_or_create(
                course_number=course_number, course_name=course_name,
                syllabus=syllabus, semester=semester, visible=visible
            )

        return obj

    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        for registration in models.Registration.objects.filter(courses=obj):
            self.publisher.notify(Registration, 'delete', obj=registration)
        for entity in models.Entity.objects.filter(course=obj):
            self.publisher.notify(Entity, 'delete', obj=entity)
        for assignment in models.Assignment.objects.filter(course=obj):
            self.publisher.notify(Assignment, 'delete', obj=assignment)

        if commit:
            obj.delete()


@register_subscriber()
class Assignment(Subscriber):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            course = kwargs.get('course')
            assignment_name = kwargs.get('assignment_name')
            description = kwargs.get('description')
            assignment_type = kwargs.get('assignment_type')
            submission_type = kwargs.get('submission_type')
            total_score = kwargs.get('total_score')
            weight = kwargs.get('weight')
            date_created = kwargs.get('date_created')
            date_released = kwargs.get('date_released')
            date_due = kwargs.get('date_due')
            review_assign_policy = kwargs.get('review_assign_policy')
            obj, _ = models.Assignment.objects.get_or_create(
                course=course, assignment_name=assignment_name,
                description=description, assignment_type=assignment_type,
                submission_type=submission_type, total_score=total_score,
                weight=weight, date_created=date_created,
                date_released=date_released, date_due=date_due,
                review_assign_policy=review_assign_policy
            )

        return obj

    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        for artifact in models.Artifact.objects.filter(assignment=obj):
            self.publisher.notify(Artifact, 'delete', obj=artifact)
        for feedback_survey in models.FeedbackSurvey.objects.filter(assignment=obj):
            self.publisher.notify(
                FeedbackSurvey, 'delete', obj=feedback_survey)

        if commit:
            obj.delete()


@register_subscriber()
class FeedbackSurvey(Subscriber):

    def create(self, obj, *args, **kwargs):
        if obj is None:
            template = kwargs.get('template')
            assignment = kwargs.get('assignment')
            date_created = kwargs.get('date_created')
            date_released = kwargs.get('date_released')
            date_due = kwargs.get('date_due')
            obj, _ = models.FeedbackSurvey.objects.get_or_create(
                template=template, assignment=assignment,
                date_created=date_created, date_released=date_released, date_due=date_due
            )

        for artifact in models.Artifact.objects.filter(assignment=obj.assignment):
            self.publisher.notify(Artifact, 'create_review', obj=artifact)

    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        for artifact in models.Artifact.objects.filter(assignment=obj.assignment):
            for artifact_review in models.ArtifactReview.objects.filter(artifact=artifact):
                self.publisher.notify(ArtifactReview, 'delete',
                                      obj=artifact_review)

        if commit:
            obj.delete()


@register_subscriber()
class Artifact(Subscriber):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            entity = kwargs.get('entity')
            assignment = kwargs.get('assignment')
            upload_time = kwargs.get('upload_time')
            file = kwargs.get('file')
            obj, _ = models.Artifact.objects.get_or_create(
                entity=entity, assignment=assignment,
                upload_time=upload_time, file=file
            )

        # Create ArtifactReview for the artifact if the feedback survey is created
        if obj.assignment.feedback_survey is not None:
            self.publisher.notify(Artifact, 'create_review', obj=obj)

        return obj

    def create_review(self, obj):
        if obj is None:
            raise ValueError("Artifact object is None")

        # If the assignment this artifact belongs to does not have a feedback survey,
        # then no need to create artifact reviews.
        if obj.assignment.survey_template is None:
            return

        course = obj.assignment.course
        cur_entity = obj.entity

        if obj.assignment.assignmentType == models.Assignment.AssigmentType.Individual:
            entities = models.Individual.objects.filter(course=course)
        else:
            entities = models.Team.objects.filter(course=course)

        # For each entity that the student is not a member of, create an artifact review
        for entity in entities:
            if entity == cur_entity:
                continue
            for member in entity.members:
                self.publisher.notify(
                    ArtifactReview, 'create', artifact=obj, user=member)

    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        for artifact_review in models.ArtifactReview.objects.filter(artifact=obj):
            self.publisher.notify(ArtifactReview, 'delete',
                                  obj=artifact_review)

        if commit:
            obj.delete()


@register_subscriber()
class ArtifactReview(Subscriber):
    def create(self, obj, *args, **kwargs):
        if obj is None:
            artifact = kwargs.get('artifact')
            user = kwargs.get('user')
            obj, _ = models.ArtifactReview.objects.get_or_create(
                artifact=artifact, user=user)

        return obj

    def update(self, obj, *args, **kwargs):
        pass

    def delete(self, obj, commit=True):
        if commit:
            obj.delete()
