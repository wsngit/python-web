from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Course, Group
from .drf_serializers import CourseSerializer, CourseDetailSerializer, GroupSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    DRF ViewSet для курсов
    """
    queryset = Course.objects.all().annotate(
        group_count=Count('groups')
    )

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def list(self, request, *args, **kwargs):
        """Переопределение list для кастомного ответа"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)

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

    def create(self, request, *args, **kwargs):
        """Переопределение create для кастомного ответа"""
        serializer = self.get_serializer(data=request.data)

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

    def update(self, request, *args, **kwargs):
        """Переопределение update для кастомного ответа"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                course = serializer.save()

                return Response({
                    'status': 'success',
                    'message': 'Course updated successfully',
                    'course': CourseSerializer(course).data
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

    def destroy(self, request, *args, **kwargs):
        """Переопределение destroy для кастомного ответа"""
        try:
            instance = self.get_object()
            course_name = instance.name
            self.perform_destroy(instance)

            return Response({
                'status': 'success',
                'message': f'Course "{course_name}" deleted successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        """Кастомное действие - группы курса"""
        course = self.get_object()
        groups = course.groups.all()
        serializer = GroupSerializer(groups, many=True)

        return Response({
            'status': 'success',
            'course': course.name,
            'groups': serializer.data
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Кастомное действие - статистика по курсам"""
        from django.db.models import Count
        stats = Course.objects.aggregate(
            total_courses=Count('id'),
            courses_with_groups=Count('id', filter=Count('groups') > 0)
        )

        return Response({
            'status': 'success',
            'statistics': stats
        })