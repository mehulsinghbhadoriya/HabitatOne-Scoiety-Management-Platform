from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('', views.complaint_list, name='list'),
    path('raise/', views.complaint_create, name='create'),
    path('<int:pk>/status/', views.complaint_update_status, name='update_status'),
]
