from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('request_info', views.request_info, name='request_info'),
]