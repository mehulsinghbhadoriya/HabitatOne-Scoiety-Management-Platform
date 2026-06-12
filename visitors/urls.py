from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('', views.visitor_list, name='list'),
    path('add/', views.visitor_create, name='create'),
]
