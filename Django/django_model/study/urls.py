from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
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