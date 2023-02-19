from django.contrib.auth.models import AbstractUser
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


class Subscription(models.Model):
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscribing', 'user'],
                name='unique_subscribing_user'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscribing')),
                name='disable_self_subscribe',
            )
        ]

    def __str__(self) -> str:
        return f'({self.user}) is subscribing on ({self.subscribing})'
