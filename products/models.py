from django.db import models
from django.core.validators import MinLengthValidator


class Product(models.Model):
    name = models.CharField(
        unique = True,
        max_length=100,
        validators=[MinLengthValidator(3, "Product name must be at least 3 characters")
    ])
    description = models.TextField(max_length=250)
    SECURITY = 'Security'
    PRODUCTIVITY = 'Productivity'
    DESIGN = 'Design'
    BUSINESS = 'Business'
    CATEGORY_CHOICES = [
        (SECURITY, 'Security'),
        (PRODUCTIVITY, 'Productivity'),
        (DESIGN, 'Design'),
        (BUSINESS, 'Business'),
    ]
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default=SECURITY,)
    LIFETIME = 'Lifetime'
    ANNUALLY = 'Annually'
    MONTHLY = 'Monthly'
    BILLING_CHOICES = [
        (LIFETIME, 'Lifetime'),
        (ANNUALLY, 'Annually'),
        (MONTHLY, 'Monthly'),
    ]
    billing_type = models.CharField(max_length=9, choices=BILLING_CHOICES, default=MONTHLY,)
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    ARCHIVED = 'Archived'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (ARCHIVED, 'Archived'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=ACTIVE,)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.name
