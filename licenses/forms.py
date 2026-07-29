from django import forms
from licenses.models import License
from customers.models import Customer
from products.models import Product


class LicenseCreateForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "customer",
            "product",
            "note",
            "status",
        ]
    def __init__(self, *args, **kwargs):
        super(LicenseCreateForm, self).__init__(*args, **kwargs)
        self.fields["customer"].queryset = Customer.objects.filter(status__exact=Customer.ACTIVE)
        self.fields["product"].queryset = Product.objects.filter(status__exact=Product.ACTIVE)

class LicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "customer",
            "product",
            "note",
            "status",
        ]
    def __init__(self, *args, **kwargs):
        super(LicenseUpdateForm, self).__init__(*args, **kwargs)
        self.fields["customer"].disabled = True
        self.fields["product"].disabled = True
        # CHANGE IT




