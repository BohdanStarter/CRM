from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='all'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
]