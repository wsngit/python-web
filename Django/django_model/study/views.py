from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Course, Student
from django.db.models import Q,Count, Avg, Max, Min

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


@require_http_methods(["GET"])
def course_list_sorted(request):
    """Список курсов с возможностью сортировки"""
    # Получаем параметр сортировки из URL
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')

    # Базовый queryset
    courses = Course.objects.all()

    # Доступные поля для сортировки
    allowed_sort_fields = {
        'name': 'name',
        'code': 'code',
        'id': 'id'
    }

    # Проверяем, что поле разрешено для сортировки
    if sort_by in allowed_sort_fields:
        field_name = allowed_sort_fields[sort_by]

        # Определяем направление сортировки
        if order == 'desc':
            field_name = f'-{field_name}'

        # Применяем сортировку
        courses = courses.order_by(field_name)
    else:
        # Сортировка по умолчанию
        courses = courses.order_by('name')

    # Формируем данные
    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'description': course.description
        })

    return JsonResponse({
        'sort_by': sort_by,
        'order': order,
        'courses': courses_data,
        'total_count': len(courses_data)
    })

@require_http_methods(["GET"])
def search_courses_by_name(request):
    """Поиск курсов по названию"""
    # Получаем параметр поиска из URL
    search_name = request.GET.get('name', '').strip()

    if not search_name:
        return JsonResponse({
            'error': 'Parameter "name" is required'
        }, status=400)

    # Ищем курсы, где название содержит искомую строку (без учета регистра)
    courses = Course.objects.filter(name__icontains=search_name)

    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'description': course.description
        })

    return JsonResponse({
        'search_term': search_name,
        'courses': courses_data,
        'found_count': len(courses_data)
    })


@require_http_methods(["GET"])
def courses_students_count(request):
    """Количество студентов, изучающих курс"""

    # Количество студентов на каждом курсе
    course_stats = Student.objects.values(
        'group__courses__name'
    ).annotate(
        student_count=Count('id', distinct=True)
    ).filter(
        group__courses__isnull=False
    ).order_by('-student_count')

    courses_data = []
    for course in course_stats:
        courses_data.append({
            'course': course['group__courses__name'],
            'student_count': course['student_count']
        })

    return JsonResponse(courses_data, safe=False)

@require_http_methods(["GET"])
def stats(request):
    """Агрегированная статистика по курсам и студентам"""

    # Агрегация по всем курсам
    stats = Course.objects.annotate(
        student_count=Count('groups__students', distinct=True)
    ).aggregate(
        total_courses=Count('id', distinct=True),
        avg_students_per_course=Avg('student_count'),
        max_students_per_course=Max('student_count'),
        min_students_per_course=Min('student_count')
    )

    # Дополнительная статистика по студентам
    student_stats = Student.objects.aggregate(
        total_students=Count('id'),
        active_students=Count('id', filter=Q(is_active=True))
    )

    response_data = {
        'courses_statistics': {
            'total_courses': stats['total_courses'],
            'average_students_per_course': round(stats['avg_students_per_course'] or 0, 1),
            'max_students_in_course': stats['max_students_per_course'] or 0,
            'min_students_in_course': stats['min_students_per_course'] or 0
        },
        'students_statistics': {
            'total_students': student_stats['total_students'],
            'active_students': student_stats['active_students']
        }
    }

    return JsonResponse(response_data)

@csrf_exempt
@require_http_methods(["GET"])
def search_courses_by_name_or_code(request):
    """Поиск курсов по названию или коду"""
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        return JsonResponse({
            'error': 'Parameter "q" is required'
        }, status=400)

    # Ищем по названию ИЛИ по коду
    courses = Course.objects.filter(
        Q(name__icontains=search_term) | Q(code__icontains=search_term)
    )

    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'description': course.description
        })

    return JsonResponse({
        'search_term': search_term,
        'courses': courses_data,
        'found_count': len(courses_data)
    })

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
