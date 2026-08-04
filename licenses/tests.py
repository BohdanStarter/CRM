from django.test import TestCase
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import timedelta
import re
from licenses.models import License
from products.models import Product
from customers.models import Customer
from licenses.forms import LicenseCreateForm, LicenseUpdateForm
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

    def test_license_create_form(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        inactive_product = Product.objects.get(name="VPN Inactive")

        active_customer = Customer.objects.get(status=Customer.ACTIVE)
        inactive_customer = Customer.objects.get(status=Customer.INACTIVE)

        form = LicenseCreateForm()

        self.assertTrue(active_customer in form.fields["customer"].queryset)
        self.assertFalse(inactive_customer in form.fields["customer"].queryset)

        self.assertTrue(product_lifetime in form.fields["product"].queryset)
        self.assertFalse(inactive_product in form.fields["product"].queryset)

    def test_license_update_form(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        license = License.objects.get(product=product_lifetime)
        form = LicenseUpdateForm(instance=license)

        self.assertIn("note", form.fields)
        self.assertIn("status", form.fields)

        self.assertTrue(form.fields["customer"].disabled)
        self.assertTrue(form.fields["product"].disabled)

        form = LicenseUpdateForm(instance=license, data={"note": "This is a test for a form", "status": License.SUSPENDED})

        self.assertTrue(form.is_valid())

        form.save()
        license.refresh_from_db()

        self.assertEqual(license.note, "This is a test for a form")
        self.assertEqual(license.status, License.SUSPENDED)

    def test_suspend_subscription_license(self):
        product_monthly = Product.objects.get(name="VPN 1 month")
        license = License.objects.get(product=product_monthly)

        # Before suspension
        self.assertEqual(license.status, License.ACTIVE)
        self.assertTrue(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertIsNone(license.suspended_at)

        license.status = License.SUSPENDED
        license.save()

        # After
        self.assertEqual(license.status, License.SUSPENDED)
        self.assertIsNone(license.expiration_date)
        self.assertTrue(license.remaining_duration)
        self.assertTrue(license.suspended_at)

        license.status = License.ACTIVE
        license.save()

        # Restored
        self.assertEqual(license.status, License.ACTIVE)
        self.assertTrue(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertIsNone(license.suspended_at)

    def test_suspend_lifetime_license(self):
        product_lifetime = Product.objects.get(name="VPN Unlimited")
        license = License.objects.get(product=product_lifetime)

        # Before suspension
        self.assertEqual(license.status, License.ACTIVE)
        self.assertIsNone(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertIsNone(license.suspended_at)

        license.status = License.SUSPENDED
        license.save()

        # After
        self.assertEqual(license.status, License.SUSPENDED)
        self.assertIsNone(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertTrue(license.suspended_at)

        license.status = License.ACTIVE
        license.save()

        # Restored
        self.assertEqual(license.status, License.ACTIVE)
        self.assertIsNone(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertIsNone(license.suspended_at)


    def test_update_status(self):
        product_monthly = Product.objects.get(name="VPN 1 month")
        license = License.objects.get(product=product_monthly)

        self.assertEqual(license.status, License.ACTIVE)

        license.update_status()
        license.refresh_from_db()

        self.assertEqual(license.status, License.EXPIRED)

    def test_change_suspended_license_to_inactive(self):
        product_monthly = Product.objects.get(name="VPN 1 month")
        license = License.objects.get(product=product_monthly)

        license.status = License.SUSPENDED
        license.save()

        # Suspended
        self.assertEqual(license.status, License.SUSPENDED)
        self.assertIsNone(license.expiration_date)
        self.assertTrue(license.remaining_duration)
        self.assertTrue(license.suspended_at)

        license.status = License.INACTIVE
        license.save()

        # Inactive
        self.assertEqual(license.status, License.INACTIVE)
        self.assertTrue(license.expiration_date)
        self.assertIsNone(license.remaining_duration)
        self.assertIsNone(license.suspended_at)

