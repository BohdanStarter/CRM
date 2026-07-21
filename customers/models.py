from django.db import models
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, "Full name must be at least 3 characters")
    ])
    email = models.EmailField(max_length = 254)
    phone_number = PhoneNumberField(blank=True)
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=ACTIVE,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)