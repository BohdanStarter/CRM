from django.urls import path
from . import views

app_name='licenses'
urlpatterns = [
    path('', views.LicenseListView.as_view(), name='all'),
    path('license/<int:pk>/', views.LicenseDetailView.as_view(), name='license_detail'),
    path('license/create/', views.LicenseCreateView.as_view(), name='license_create'),
    path('license/<int:pk>/update/', views.LicenseUpdateView.as_view(), name='license_update'),
    path('license/<int:pk>/delete', views.LicenseDeleteView.as_view(), name='license_delete'),
]