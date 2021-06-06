"""
Accounts app models
"""
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    """User model Extending AbstractUser"""
    is_restaurant = models.BooleanField(_('Restaurant'), default=False)
    is_employee = models.BooleanField(_('Employee'), default=True)
