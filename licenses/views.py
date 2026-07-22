# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from licenses.models import License
from licenses.forms import LicenseForm
# Create your views here.


class LicenseListView(LoginRequiredMixin, ListView):
    model = License


class LicenseDetailView(LoginRequiredMixin, DetailView):
    model = License

class LicenseCreateView(LoginRequiredMixin, CreateView):
    model = License
    form_class = LicenseForm
    template_name = "licenses/license_form.html"
    success_url = reverse_lazy("licenses:all")

class LicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = License
    form_class = LicenseForm
    template_name = "licenses/license_form.html"
    success_url = reverse_lazy("licenses:all")

class LicenseDeleteView(LoginRequiredMixin, DeleteView):
    model = License
    template_name = "licenses/license_delete_confirmation.html"
    success_url = reverse_lazy("licenses:all")