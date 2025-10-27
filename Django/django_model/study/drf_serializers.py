from rest_framework import serializers
from .models import Course, Group

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""
    group_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'group_count']
        read_only_fields = ['id', 'group_count']

    def get_group_count(self, obj):
        """Количество групп на курсе"""
        return obj.groups.count()

    def validate_code(self, value):
        """Валидация кода курса"""
        if len(value) < 2:
            raise serializers.ValidationError("Код курса должен содержать минимум 2 символа")
        return value

    def validate(self, data):
        """Валидация на уровне всех полей"""
        # Проверяем, что название и код не совпадают
        if data.get('name') and data.get('code'):
            if data['name'].lower() == data['code'].lower():
                raise serializers.ValidationError({
                    'name': 'Название и код курса не должны совпадать'
                })
        return data

class CourseDetailSerializer(CourseSerializer):
    """Расширенный сериализатор для детального просмотра курса"""
    groups = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['groups']

    def get_groups(self, obj):
        """Список групп на курсе"""
        from .drf_serializers import GroupSerializer
        groups = obj.groups.all()
        return GroupSerializer(groups, many=True).data

class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для группы"""
    course_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'code', 'course_count', 'student_count']
        read_only_fields = ['id', 'course_count', 'student_count']

    def get_course_count(self, obj):
        """Количество курсов в группе"""
        return obj.courses.count()

    def get_student_count(self, obj):
        """Количество студентов в группе"""
        return obj.students.count()