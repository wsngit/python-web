from django.urls import path
from . import views


urlpatterns = [
    # Наследование и включение шаблонов
    path('', views.home, name='home'),

    # Работа с формами - тест
    path('test/', views.python_test_view, name='python_test'),

    # Работа с медиа-файлами - галерея
    path('gallery/', views.simple_gallery_view, name='gallery'),
    path('gallery/delete/<str:filename>/', views.delete_image, name='delete_image'),
    path('gallery/clear/', views.clear_gallery, name='clear_gallery'),
]

