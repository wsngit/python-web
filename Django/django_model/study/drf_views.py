from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course
from .drf_serializers import CourseSerializer, CourseDetailSerializer

@api_view(['GET'])
def drf_course_list(request):
    """
    Список всех курсов
    """
    try:
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response({
            'status': 'success',
            'count': len(serializer.data),
            'courses': serializer.data
        })

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def drf_course_create(request):
    """
    Создать новый курс
    """
    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        try:
            course = serializer.save()

            return Response({
                'status': 'success',
                'message': 'Course created successfully',
                'course': CourseSerializer(course).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'status': 'error',
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def drf_course_detail(request, course_id):
    """
    GET - детали курса
    PUT - изменение курса
    DELETE - удаление курса
    """
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'GET':
        try:
            serializer = CourseDetailSerializer(course)

            return Response({
                'status': 'success',
                'course': serializer.data
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data, partial=False)

        if serializer.is_valid():
            try:
                updated_course = serializer.save()

                return Response({
                    'status': 'success',
                    'message': 'Course updated successfully',
                    'course': CourseSerializer(updated_course).data
                })

            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': 'error',
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            course_name = course.name
            course.delete()

            return Response({
                'status': 'success',
                'message': f'Course "{course_name}" deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)