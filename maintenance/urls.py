from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.bill_list, name='list'),
    path('create/', views.bill_create, name='create'),
    path('<int:pk>/edit/', views.bill_edit, name='edit'),
    path('<int:pk>/delete/', views.bill_delete, name='delete'),
    path('<int:pk>/mark-paid/', views.mark_paid, name='mark_paid'),
]
