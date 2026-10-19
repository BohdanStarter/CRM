from django.db import models
from customers.models import Customer
from licenses.models import License
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# import logging

# logger = logging.getLogger(__name__)

class Activity(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="activities")
    related_license = models.ForeignKey(License, on_delete=models.SET_NULL, related_name="activities", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="activities")
    updated_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, related_name="activities_upd")

    CHAT = 'Chat'
    CALL = 'Call'
    EMAIL = 'Email'
    MEET = 'Meet'
    QUICK_NOTE = 'Quick note'

    ACTIVITY_CHOICES = [
        (CHAT, 'Chat'),
        (CALL, 'Call'),
        (EMAIL, 'Email'),
        (MEET, 'Meet'),
        (QUICK_NOTE, 'Quick note')
    ]

    occurred_at = models.DateTimeField(default=timezone.now)
    subject = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default=CHAT)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      ordering = ['-occurred_at']

    def clean(self):
        checks = {}
        if self.related_license and self.customer_id is not None:
            if self.related_license.customer_id != self.customer_id:
                checks.update(
                    {"related_license": "License should be related to the same customer."}
                )
        if self.occurred_at is not None:
            if self.occurred_at > timezone.now():
                checks.update(
                    {"occurred_at": "Date should be now or earlier."}
                )
        if checks != {}:
            raise ValidationError(checks)


    def __str__(self):
        if self.customer_id:
            activity_name = f'{self.customer.full_name} {self.activity_type} {self.subject}'
        else:
            activity_name =  f'Customer {self.activity_type} {self.subject}'
        return activity_name