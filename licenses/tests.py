from django.test import TestCase
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
import re
from licenses.models import License
from products.models import Product
from customers.models import Customer
# Create your tests here.


class LicenseTestCase(TestCase):
    def setUp(self):
        test_customer = Customer.objects.create(
            full_name="Test Customer",
            email="test@gmail.com",
            status=Customer.ACTIVE,
        )

        Customer.objects.create(
            full_name="Test Inactive Customer",
            email="test_inactive@gmail.com",
            status=Customer.INACTIVE,
        )

        Product.objects.create(
            name="VPN Inactive",
            description="VPN protection for your devices. (Inactive)",
            category=Product.SECURITY,
            billing_type=Product.ANNUALLY,
            status=Product.INACTIVE,
            price="10"
        )

        product_lifetime = Product.objects.create(
            name="VPN Unlimited",
            description="VPN protection for your devices",
            category=Product.SECURITY,
            billing_type=Product.LIFETIME,
            status=Product.ACTIVE,
            price="100"
        )
        product_month = Product.objects.create(
            name="VPN 1 month",
            description="VPN protection for your devices",
            category=Product.SECURITY,
            billing_type=Product.MONTHLY,
            status=Product.ACTIVE,
            price="10"
        )
        product_year = Product.objects.create(
            name="VPN 1 year",
            description="VPN protection for your devices",
            category=Product.SECURITY,
            billing_type=Product.ANNUALLY,
            status=Product.ACTIVE,
            price="35"
        )
        License.objects.create(
            customer=test_customer,
            product=product_lifetime,
            status=License.ACTIVE,
        )
        License.objects.create(
            customer=test_customer,
            product=product_month,
            status=License.ACTIVE,
        )
        License.objects.create(
            customer=test_customer,
            product=product_year,
            status=License.ACTIVE,
        )

    def test_key_generated(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        product_year = Product.objects.get(name="VPN 1 year")
        product_month = Product.objects.get(name="VPN 1 month")

        lifetime = License.objects.get(product=product_lifetime)
        year = License.objects.get(product=product_year)
        month = License.objects.get(product=product_month)
        print("Method: test_key_generated passed the test.")
        self.assertTrue(lifetime.license_key)
        self.assertTrue(year.license_key)
        self.assertTrue(month.license_key)



    def test_expiration_date(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        product_year = Product.objects.get(name="VPN 1 year")
        product_month = Product.objects.get(name="VPN 1 month")

        lifetime = License.objects.get(product=product_lifetime)
        year = License.objects.get(product=product_year)
        month = License.objects.get(product=product_month)
        print("Method: test_expiration_date passed the test.")

        # Check if expiration date is added automatically
        self.assertTrue(year.expiration_date)
        self.assertTrue(month.expiration_date)

        # Check if expiration date set properly
        self.assertIsNone(lifetime.expiration_date)
        self.assertAlmostEqual(year.expiration_date, timezone.now() + relativedelta(years=1), delta=timedelta(seconds=2))
        self.assertAlmostEqual(month.expiration_date, timezone.now() + relativedelta(months=1), delta=timedelta(seconds=2))

    def test_is_expired(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        product_year = Product.objects.get(name="VPN 1 year")
        product_month = Product.objects.get(name="VPN 1 month")

        lifetime = License.objects.get(product=product_lifetime)
        year = License.objects.get(product=product_year)
        month = License.objects.get(product=product_month)

        self.assertFalse(lifetime.is_expired)
        self.assertFalse(year.is_expired)
        self.assertFalse(month.is_expired)

    def test_is_expired_expired(self):
        product_year = Product.objects.get(name="VPN 1 year")
        product_month = Product.objects.get(name="VPN 1 month")

        year = License.objects.get(product=product_year)
        month = License.objects.get(product=product_month)

        year.expiration_date=(timezone.now() - relativedelta(days=1))
        year.save()
        month.expiration_date=(timezone.now() - relativedelta(days=1))
        month.save()

        self.assertTrue(year.is_expired)
        self.assertTrue(month.is_expired)

    def test_license_key(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        product_year = Product.objects.get(name="VPN 1 year")
        product_month = Product.objects.get(name="VPN 1 month")

        lifetime = License.objects.get(product=product_lifetime)
        year = License.objects.get(product=product_year)
        month = License.objects.get(product=product_month)

        key_structure = r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}"

        self.assertTrue(bool(re.fullmatch(key_structure, lifetime.license_key)))
        self.assertTrue(bool(re.fullmatch(key_structure, year.license_key)))
        self.assertTrue(bool(re.fullmatch(key_structure, month.license_key)))

    def test_license_validation(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        inactive_product = Product.objects.get(name="VPN Inactive")

        active_customer = Customer.objects.get(status=Customer.ACTIVE)
        inactive_customer = Customer.objects.get(status=Customer.INACTIVE)

        with self.assertRaises(ValidationError):
            license = License(customer=inactive_customer)
            license.full_clean()

        with self.assertRaises(ValidationError):
            license = License(customer=active_customer, product=inactive_product)
            license.full_clean()


        lifetime = License.objects.get(product=product_lifetime)
        self.assertFalse(lifetime.full_clean())

        # License with inactive product/customer can still be changed

        product_lifetime.status = Product.INACTIVE
        product_lifetime.save()

        lifetime.status = License.INACTIVE
        lifetime.save()

        self.assertFalse(lifetime.full_clean())














