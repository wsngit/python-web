from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile_detailed, name='user_profile_detailed'),
    path('password/change/',
         auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'),
         name='password_change'),
]