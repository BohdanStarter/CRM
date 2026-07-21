from django import forms
from customers.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "full_name",
            "email",
            "phone_number",
            "status",
        ]