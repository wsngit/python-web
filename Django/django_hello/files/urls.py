from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_file, name='upload_file'),
    path('uploads/<str:filename>/', views.get_file, name='get_file'),
]