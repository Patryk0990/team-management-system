from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.utils import UserManager
from utils.fields import ImageField


class User(AbstractBaseUser):
    first_name = models.CharField(_('first name'), max_length=64)
    last_name = models.CharField(_('last name'), max_length=64)
    email = models.EmailField(_('email address'), unique=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    avatar = ImageField(
        _('avatar'),
        default='accounts/avatars/default.png',
        upload_to='accounts/avatars/',
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(_('phone number'), null=True, blank=True, unique=True)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'accounts/avatars/default.png'
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
