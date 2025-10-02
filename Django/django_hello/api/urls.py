# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world),
    path('greet/', views.hello_name),

    path('hello/<str:name>/', views.hello),

    path('params/', views.params),

]


