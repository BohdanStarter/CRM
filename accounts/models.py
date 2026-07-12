from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    SALES = 'SALES'
    SUPPORT = 'SUPPORT'

    ROLE_CHOICES = [
      (SALES, 'Sales'),
      (SUPPORT, 'Support'),
    ]

    role = models.CharField(
        max_length = 7,
        choices=ROLE_CHOICES,
        default=SALES,
    )