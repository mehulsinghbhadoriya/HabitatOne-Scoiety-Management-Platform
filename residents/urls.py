from django.urls import path
from . import views

app_name = 'residents'

urlpatterns = [
    path('', views.resident_list, name='list'),
    path('add/', views.resident_create, name='create'),
    path('<int:pk>/edit/', views.resident_edit, name='edit'),
    path('<int:pk>/delete/', views.resident_delete, name='delete'),
    path('<int:pk>/', views.resident_detail, name='detail'),
]
