from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Course

@csrf_exempt
@require_http_methods(["GET"])
def course_list(request):
    """
    GET - получить список всех курсов
    """
    try:
        courses = Course.objects.all()

        courses_data = []
        for course in courses:
            courses_data.append({
                'id': course.id,
                'name': course.name,
                'code': course.code,
                'description': course.description,
                'group_count': course.groups.count(),
            })

        return JsonResponse({
            'status': 'success',
            'count': len(courses_data),
            'courses': courses_data
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course_detail(request, course_id):
    """
    GET - получить детали курса
    PUT - обновить курс
    DELETE - удалить курс
    """
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'GET':
        try:
            data = {
                'id': course.id,
                'name': course.name,
                'code': course.code,
                'description': course.description,
                'group_count': course.groups.count(),
            }

            return JsonResponse({
                'status': 'success',
                'course': data
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # Проверяем обязательные поля
            if not data.get('name') or not data.get('code'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Name and code are required'
                }, status=400)

            # Проверяем уникальность кода
            if Course.objects.filter(code=data['code']).exclude(id=course_id).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Course with this code already exists'
                }, status=400)

            # Обновляем курс
            course.name = data['name']
            course.code = data['code']
            course.description = data.get('description', '')
            course.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Course updated successfully',
                'course': {
                    'id': course.id,
                    'name': course.name,
                    'code': course.code,
                    'description': course.description
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    elif request.method == 'DELETE':
        try:
            course_name = course.name
            course.delete()

            return JsonResponse({
                'status': 'success',
                'message': f'Course "{course_name}" deleted successfully'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def course_create(request):
    """
    Создать новый курс
    """
    try:
        data = json.loads(request.body)

        # Проверяем обязательные поля
        if not data.get('name') or not data.get('code'):
            return JsonResponse({
                'status': 'error',
                'message': 'Name and code are required'
            }, status=400)

        # Проверяем уникальность кода
        if Course.objects.filter(code=data['code']).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Course with this code already exists'
            }, status=400)

        # Создаем курс
        course = Course.objects.create(
            name=data['name'],
            code=data['code'],
            description=data.get('description', '')
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Course created successfully',
            'course': {
                'id': course.id,
                'name': course.name,
                'code': course.code,
                'description': course.description
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
