# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import BlockSalesMixin, BlockSupportMixin
from customers.models import Customer
from customers.forms import CustomerForm
# Create your views here.


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 10


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer

class CustomerCreateView(LoginRequiredMixin, BlockSalesMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:all")

class CustomerUpdateView(LoginRequiredMixin, BlockSalesMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:all")

class CustomerDeleteView(LoginRequiredMixin, BlockSalesMixin, BlockSupportMixin, DeleteView):
    model = Customer
    template_name = "customers/customer_delete_confirmation.html"
    success_url = reverse_lazy("customers:all")