from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class User(AbstractUser):
    ADMIN = 'Admin'
    SALES = 'Sales'
    SUPPORT = 'Support'

    ROLE_CHOICES = [
      (ADMIN, 'Admin'),
      (SALES, 'Sales'),
      (SUPPORT, 'Support'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=SALES,
    )

    @property
    def is_admin(self):
        if self.role == self.ADMIN or self.role == "ADMIN":
            return True
        else:
            return False

    @property
    def is_support(self):
        return self.role == self.SUPPORT

    @property
    def is_sales(self):
        return self.role == self.SALES

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        try:
            target_group = Group.objects.get(name=self.role)
            all_role_names = [self.ADMIN, self.SALES, self.SUPPORT]
            roles_to_remove = Group.objects.filter(name__in=all_role_names).exclude(name=self.role)
            self.groups.remove(*roles_to_remove)
            self.groups.add(target_group)

        except Group.DoesNotExist:
            pass