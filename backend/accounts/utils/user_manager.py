from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from utils import MailService

if TYPE_CHECKING:
    from accounts.models import User


class UserManager(BaseUserManager):
    def _create_user(
            self, email: str, first_name: str, last_name: str, password: str = None, **extra_fields: object
    ) -> User:
        if not email:
            raise ValueError(_('Email is required.'))
        if not password:
            raise ValueError(_('Password is required.'))
        if not first_name:
            raise ValueError(_('First name is required.'))
        if not last_name:
            raise ValueError(_('Last name is required.'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(
            self, email: str, first_name: str, last_name: str, password: str = None, **extra_fields: object
    ) -> User:
        user = self._create_user(email, first_name, last_name, password, **extra_fields)
        MailService.send_email_verification_mail(user)
        return user

    def create_superuser(
            self, email: str, first_name: str, last_name: str, password: str = None, **extra_fields: object
    ) -> User:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, first_name, last_name, password, **extra_fields)
