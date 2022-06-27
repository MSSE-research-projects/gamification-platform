from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from .models import CustomUser, Course, Assignment


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

    def save(self, commit=True):
        user = super().save(commit=True)
        if commit:
            user.save()
        return user


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('course_id', 'course_name', 'syllabus',
                  'semester', 'visible')

    def save(self, commit=True):
        course = super().save(commit=True)
        if commit:
            course.save()
        return course
    
class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ('course_id', 'assignment_name', 'description',
                  'assignment_type', 'submission_type', 'total_score',
                  'weight', 'date_created', 'date_released', 'date_due','review_assign_policy')

    def save(self, commit=True):
        assignment = super().save(commit=True)
        if commit:
            assignment.save()
        return assignment
