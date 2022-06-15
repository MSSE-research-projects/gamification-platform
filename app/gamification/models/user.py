from email.policy import default
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username_validator = ASCIIUsernameValidator()

    andrew_id = models.CharField(
        _('Andrew ID'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Lower case letters only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that andrew id already exists.'),
        },
    )
    image = models.ImageField(_('profile picture'),
                              upload_to='profile_pics', blank=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('data joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'andrew_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        # db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        '''
        Return the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return f'{self.get_full_name()}'

    def get_short_name(self):
        '''Return the short name for the user.'''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''Send an email to this user.'''
        send_mail(subject, message, from_email, [self.email], **kwargs)
