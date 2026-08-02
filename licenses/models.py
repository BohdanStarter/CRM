import secrets
import string
from django.utils.translation import gettext_lazy as gl
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
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
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, related_name="licenses")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name="licenses")
    license_key = models.CharField(max_length=19, unique=True, editable=False)
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
    suspended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remaining_duration = models.DurationField(null=True, blank=True, editable=False)


    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = self.generate_unique_license_key()

        if self.expiration_date is None and self.product.billing_type != Product.LIFETIME and self.status != self.SUSPENDED:
            self.expiration_date = self.expiration()

        if self.suspended_at is None and self.status == self.SUSPENDED and self.product.billing_type != Product.LIFETIME:
            self.suspended_at = timezone.now()
            self.handle_suspension_duration()
            self.expiration_date = None
        elif self.suspended_at and self.status == self.ACTIVE:
            if self.product.billing_type != Product.LIFETIME:
                self.handle_suspension_duration()
            self.suspended_at = None
        elif self.suspended_at is None and self.status == self.SUSPENDED and self.product.billing_type == Product.LIFETIME:
            self.suspended_at = timezone.now()
            self.expiration_date = None
            self.remaining_duration = None

        if self.status == self.INACTIVE:
            self.suspended_at = None
            self.remaining_duration = None

        super().save(*args, **kwargs)

    def clean(self):
        if not self.pk:
            if self.customer.status == Customer.INACTIVE:
                raise ValidationError(
                    {"customer": gl("Customer should have an active status.")}
                )
            if self.product.status == Product.INACTIVE or self.product.status == Product.ARCHIVED:
                raise ValidationError(
                    {"product": gl("Product should have an active status.")}
                )

    def generate_unique_license_key(self):
        while True:
            new_key = generate_license_key()
            if not License.objects.filter(license_key=new_key).exists():
                return new_key

    def expiration(self):
        if self.product.billing_type == Product.LIFETIME:
            expiration_date = None
        elif self.product.billing_type == Product.MONTHLY:
            expiration_date = timezone.now() + relativedelta(months=1)
        elif self.product.billing_type == Product.ANNUALLY:
            expiration_date = timezone.now() + relativedelta(years=1)
        else:
            raise ValueError("Unknown value of billing type.")
        return expiration_date


    def handle_suspension_duration(self):
        if not self.remaining_duration:
            self.remaining_duration = self.expiration_date - timezone.now()
        else:
            self.expiration_date = timezone.now() + self.remaining_duration
            self.remaining_duration = None

    def update_status(self):
        if self.is_expired and self.status == self.ACTIVE:
            self.status = self.EXPIRED
            self.save(update_fields=["status"])


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

