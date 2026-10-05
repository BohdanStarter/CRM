# from django.shortcuts import render
import logging
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from accounts.mixins import BlockSalesMixin, BlockSupportMixin
from licenses.models import License
from licenses.forms import LicenseCreateForm, LicenseUpdateForm

logger = logging.getLogger(__name__)

class LicenseListView(LoginRequiredMixin, ListView):
    model = License
    paginate_by = 10
    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            query = Q(customer__full_name__icontains=search)
            query.add(Q(customer__email__icontains=search), Q.OR)
            query.add(Q(note__icontains=search), Q.OR)
            query.add(Q(product__name__icontains=search), Q.OR)
            query.add(Q(status__iexact=search), Q.OR)
            return License.objects.filter(query).distinct().order_by("-updated_at")
        else:
            return License.objects.all().order_by("-updated_at")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = search
        context['search_link'] = f"&search={search}" if search else ""
        return context



class LicenseDetailView(LoginRequiredMixin, DetailView):
    model = License

    def post(self, request, *args, **kwargs):
        # 1. Get the object standard DetailView style
        self.license = self.get_object()

        # 2. Check if the specific button was clicked
        if 'renew_button' in request.POST:
            self.license.renew()
            logger.info(f"License (ID:{self.license.pk}, Name: {self.license.customer}, Product: {self.license.product}) was renewed!")


            messages.success(request, "The license has been successfully renewed.")
            return redirect('licenses:license_detail', pk=self.license.pk)


class LicenseCreateView(LoginRequiredMixin, BlockSalesMixin, BlockSupportMixin, CreateView):
    model = License
    form_class = LicenseCreateForm
    template_name = "licenses/license_form.html"
    success_url = reverse_lazy("licenses:all")

class LicenseUpdateView(LoginRequiredMixin, BlockSalesMixin, BlockSupportMixin, UpdateView):
    model = License
    form_class = LicenseUpdateForm
    template_name = "licenses/license_form.html"
    success_url = reverse_lazy("licenses:all")

class LicenseDeleteView(LoginRequiredMixin, BlockSalesMixin, BlockSupportMixin, DeleteView):
    model = License
    template_name = "licenses/license_delete_confirmation.html"
    success_url = reverse_lazy("licenses:all")