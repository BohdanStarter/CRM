from django.urls import path
from . import views

app_name='customers'
urlpatterns = [
    path('', views.CustomerListView.as_view(), name='all'),
    path('customer/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/<int:pk>/delete', views.CustomerDeleteView.as_view(), name='customer_delete'),
]