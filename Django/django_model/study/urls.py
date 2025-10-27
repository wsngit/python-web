from django.urls import path, include
from . import views, drf_views
from rest_framework.routers import DefaultRouter
from .drf_viewset import CourseViewSet


# Создаем router для ViewSet
router = DefaultRouter()
router.register(r'drf/v2/courses', CourseViewSet, basename='course')

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    #Сортировка
    path('courses/sort/', views.course_list_sorted, name='course_list_sorted'),

    #Поиск по полям
    path('courses/search/by-name/', views.search_courses_by_name, name='search_courses_by_name'),    # Простой фильтр
    path('courses/search/', views.search_courses_by_name_or_code, name='search_courses'),            # Q-объекты
    path('courses/students_count/', views.courses_students_count, name='students_count_on_course'),  # Количество студентов на каждом курсе
    path('stats', views.stats, name='stats'),                                                        # Cтатистика

    #DRF urls
    path('drf/courses/', drf_views.drf_course_list, name='drf_course_list'),
    path('drf/courses/create/', drf_views.drf_course_create, name='drf_course_create'),
    path('drf/courses/<int:course_id>/', drf_views.drf_course_detail, name='drf_course_detail'),

    # DRF ViewSet URLs (автогенерация)
    path('', include(router.urls)),
]

#Создание курса
#curl -X POST http://localhost:8000/study/courses/create/ \
#-H "Content-Type: application/json" \
#-d '{
#  name": "Python Programming",
#  "code": "PY101",
#  "description": "Introduction to Python programming"
#}'

#Получение списка курсов
#curl -X GET http://localhost:8000/study/courses/

#Получение списка курсов c сортировкой
#curl "http://localhost:8000/study/courses/sorted/?sort=name&order=asc"

#Поиск по имени или коду курса
#curl "http://localhost:8000/study/courses/search/?q=PY"

#Количество студентов на каждом курсе
#curl http://localhost:8000/study/courses/students_count/

#Статистика
#curl http://localhost:8000/study/stats

#Получение деталей курса
#curl -X GET http://localhost:8000/study/courses/1/

#Обновление курса
#curl -X PUT http://localhost:8000/study/courses/1/ \
#-H "Content-Type: application/json" \
#-d '{
#"name": "Python",
#"code": "PY102",
#"description": "Python programming concepts"
#}'

#Удаление курса
#curl -X DELETE http://localhost:8000/study/courses/1/