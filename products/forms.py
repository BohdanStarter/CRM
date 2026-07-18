from django import forms
from products.models import Product


class CreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "billing_type",
            "status",
            "price",
        ]