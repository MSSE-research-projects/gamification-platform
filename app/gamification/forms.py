import json
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext, gettext_lazy as _

from .models import Assignment, CustomUser, Course, Registration, Team, Membership

class SignUpForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match.")
    }

    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_('Enter the same password as before, for verification'),
    )

    class Meta:
        model = CustomUser
        fields = ('andrew_id', 'email',)
        field_classes = {'andrew_id': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'image')


class CourseForm(forms.ModelForm):

    error_messages = {
        'invalid_format': _('File format is not correct. Please check the file \
            format. Make sure that the file contains the following columns: \
            Student ID, Email, Team Name.'),
        'course_name_empty': _("Course name cannot be empty."),
        'course_number_empty': _("Course number cannot be empty."),
    }

    file = forms.FileField(
        label=_('CATME file'),
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['json'])]
    )

    class Meta:
        model = Course
        fields = ('course_number', 'course_name', 'syllabus',
                  'semester', 'visible')
    
    def clean_course_number(self):
        course_number = self.cleaned_data.get('course_number')
        if course_number == '':
            raise ValidationError(
                self.error_messages['course_number_empty'],
                code='course_number_empty',
            )
        return course_number

    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')
        if course_name == '':
            raise ValidationError(
                self.error_messages['course_name_empty'],
                code='course_name_empty',
            )
        return course_name


    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file is None:
            return file

        data = json.loads(file.read())
        for row in data:
            if 'Student ID' not in row or 'Email' not in row or 'Team Name' not in row:
                raise ValidationError(
                    self.error_messages['invalid_format'],
                    code='invalid_format'
                )

        return file

    def _register_teams(self, course):
        # Register teams from CATME file
        file = self.cleaned_data.get('file')
        if file is None:
            return

        data = json.loads(file.read())

        for row in data:
            name = row.get('Name', None).strip()
            andrew_id = row['Student ID'].strip()
            email = row['Email'].strip()
            team_name = row['Team Name'].strip()

            # Get user or create one
            try:
                user = CustomUser.objects.get(andrew_id=andrew_id)
            except CustomUser.DoesNotExist:
                if name:
                    first_name, last_name = name.split(' ')
                else:
                    first_name = last_name = ''
                user = CustomUser.objects.create_user(
                    andrew_id=andrew_id,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

                password = CustomUser.objects.make_random_password()
                user.set_password(password)
                user.save()

            # Register this user to the course
            registration = Registration(
                users=user,
                courses=course,
                userRole=Registration.UserRole.Student
            )
            registration.save()

            # Do not create team if the name is empty
            if team_name == '':
                continue

            # Get team or create one
            try:
                team = Team.objects.get(course=course, name=team_name)
            except Team.DoesNotExist:
                team = Team(course=course, name=team_name)
                team.save()

            # Register this user to the team
            membership = Membership(student=registration, entity=team)
            membership.save()

    def save(self, commit=True):
        course = super().save(commit=True)
        self._register_teams(course)

        return course


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ('course', 'assignment_name', 'description',
                  'assignment_type', 'submission_type', 'total_score',
                  'weight', 'date_created', 'date_released', 'date_due', 'review_assign_policy')
        widgets = {
            'course': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('name', 'course')
