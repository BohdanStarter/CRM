from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from licenses.models import License
from customers.models import Customer
from products.models import Product
# Create your views here.


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate date helpers
        now = timezone.now()
        future_limit = now + timedelta(days=14)
        past_limit = now - timedelta(days=14)

        context['license_amount'] = License.objects.count()
        context['customer_amount'] = Customer.objects.count()
        context['product_amount'] = Product.objects.count()
        context['active_license_amount'] = License.objects.filter(status=License.ACTIVE).count()
        context['expired_license_amount'] = License.objects.filter(status=License.EXPIRED).count()
        context['suspended_license_amount'] = License.objects.filter(status=License.SUSPENDED).count()
        context['expire_list'] = License.objects.filter(status=License.ACTIVE, expiration_date__gte=now, expiration_date__lte=future_limit).order_by('expiration_date')[:10]
        context['recent_list'] = License.objects.filter(status=License.ACTIVE, purchase_date__gte=past_limit, purchase_date__lte=now).order_by('-purchase_date')[:10]
        context['recent_customer'] = Customer.objects.filter(status=Customer.ACTIVE, created_at__gte=past_limit, created_at__lte=now).order_by('-created_at')[:10]
        return context