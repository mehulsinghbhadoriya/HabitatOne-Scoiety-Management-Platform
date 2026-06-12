from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_home, name='admin_home'),
    path('resident/', views.resident_home, name='resident_home'),
]
