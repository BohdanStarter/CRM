from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from products.models import Product
from products.forms import CreateForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    # template_name = "products/products_list.html"

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    # template_name = "products/product_detail.html"

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = CreateForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:all")

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = CreateForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:all")

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_delete_confirmation.html"
    success_url = reverse_lazy("products:all")