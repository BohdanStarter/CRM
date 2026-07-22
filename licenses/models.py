import secrets
import string
from django.utils import timezone
from datetime import timedelta
from django.db import models
from products.models import Product
from customers.models import Customer

LICENSE_KEY_LENGTH = 16

def generate_license_key():
    license_key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(LICENSE_KEY_LENGTH)) + '-'
    separator = "-"
    key = ""
    for i in range(0, len(license_key), 4):
        key += license_key[i:i + 4] + separator
    key = key[:-3]
    return key

class License(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="licenses")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="licenses")
    license_key = models.CharField(max_length=LICENSE_KEY_LENGTH, unique=True, editable=False)
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    SUSPENDED = 'Suspended'
    EXPIRED = 'Expired'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (SUSPENDED, 'Suspended'),
        (EXPIRED, 'Expired'),
    ]
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=ACTIVE,)
    note = models.TextField(blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = self.generate_unique_license_key()

        if not self.expiration_date:
            self.expiration_date = self.expiration()
        super().save(*args, **kwargs)

    def generate_unique_license_key(self):
        while True:
            new_key = generate_license_key()
            if not License.objects.filter(license_key=new_key).exists():
                return new_key

    def expiration(self):
        if self.product.billing_type == Product.LIFETIME:
            expiration_date = None
        elif self.product.billing_type == Product.MONTHLY:
            expiration_date = timezone.now() + timedelta(days=30)
        elif self.product.billing_type == Product.ANNUALLY:
            expiration_date = timezone.now() + timedelta(days=365)
        else:
            raise ValueError("Unknown value of billing type.")
        return expiration_date

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_expired(self):
        if self.expiration_date is not None:
            if timezone.now() > self.expiration_date:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        license_name = self.product.name + ' ' + self.customer.full_name
        return license_name

