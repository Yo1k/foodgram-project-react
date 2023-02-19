from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return (
            f'username={self.username}, '
            f'email={self.email}, '
            f'is_staff={self.is_staff}'
        )
