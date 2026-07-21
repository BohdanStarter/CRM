from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from products.models import Product
from products.forms import ProductForm

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    # template_name = "products/product_list.html"
    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            query = Q(name__icontains=search)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(status__icontains=search), Q.OR)
            return Product.objects.filter(query).distinct().order_by("-updated_at")
        else:
            return Product.objects.all().order_by("-updated_at")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = search
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    # template_name = "products/product_detail.html"

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:all")

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:all")

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_delete_confirmation.html"
    success_url = reverse_lazy("products:all")