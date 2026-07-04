# resume_builder/urls.py
from django.urls import path
from . import views

app_name = 'resume_builder'  # این برای استفاده در {% url %} ضروری است

urlpatterns = [
    path('create/', views.resume_create, name='create'),
    path('<int:pk>/', views.resume_detail, name='detail'),
    path('<int:pk>/edit/', views.resume_edit, name='edit'),
    path('<int:pk>/delete/', views.resume_delete, name='delete'),
]