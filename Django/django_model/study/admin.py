from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Group, Student, StudentInfo

class CourseInline(admin.TabularInline):
    """Inline для отображения курсов в группе"""
    model = Group.courses.through
    extra = 1
    verbose_name = "Курс"
    verbose_name_plural = "Курсы группы"

class StudentInline(admin.TabularInline):
    """Inline для отображения студентов в группе"""
    model = Student
    extra = 0
    fields = ['student_id', 'first_name', 'last_name', 'is_active']
    readonly_fields = ['student_id', 'first_name', 'last_name']
    can_delete = False
    show_change_link = True

class StudentInfoInline(admin.StackedInline):
    """Inline для отображения информации о студенте"""
    model = StudentInfo
    can_delete = False
    verbose_name_plural = "Информация о студенте"
    fields = ['email', 'phone', 'date_of_birth', 'address']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'group_count', 'description_short']
    list_filter = ['groups']
    search_fields = ['name', 'code', 'description']
    filter_horizontal = []  # Для ManyToMany обычно не нужно в курсах

    def group_count(self, obj):
        return obj.groups.count()
    group_count.short_description = 'Количество групп'

    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    description_short.short_description = 'Описание'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'courses_list', 'student_count_display', 'is_active_display']
    list_filter = ['courses']
    search_fields = ['name', 'code']
    filter_horizontal = ['courses']
    inlines = [CourseInline, StudentInline]

    def courses_list(self, obj):
        courses = obj.courses.all()
        if courses:
            return ", ".join([course.name for course in courses])
        return "Нет курсов"
    courses_list.short_description = 'Курсы'

    def student_count_display(self, obj):
        count = obj.student_count
        color = 'green' if count > 0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            f"{count} студентов"
        )
    student_count_display.short_description = 'Количество студентов'

    def is_active_display(self, obj):
        active_students = obj.students.filter(is_active=True).count()
        total_students = obj.student_count
        if total_students == 0:
            return format_html('<span style="color: gray;">Нет студентов</span>')

        percentage = (active_students / total_students) * 100
        color = 'green' if percentage > 70 else 'orange' if percentage > 30 else 'red'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}% активных</span>',
            color,
            int(percentage)
        )
    is_active_display.short_description = 'Активность'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id',
        'last_name',
        'first_name',
        'group_display',
        'email_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'group', 'group__courses', 'created_at']
    search_fields = ['first_name', 'last_name', 'student_id', 'info__email']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [StudentInfoInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('student_id', 'first_name', 'last_name', 'group')
        }),
        ('Системная информация', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def group_display(self, obj):
        if obj.group:
            return format_html(
                '<a href="/admin/study/group/{}/change/">{}</a>',
                obj.group.id,
                obj.group.name
            )
        return format_html('<span style="color: red;">Не назначена</span>')
    group_display.short_description = 'Группа'

    def email_display(self, obj):
        if hasattr(obj, 'info') and obj.info.email:
            return obj.info.email
        return format_html('<span style="color: red;">Нет email</span>')
    email_display.short_description = 'Email'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('group', 'info')

@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = [
        'student_display',
        'email',
        'phone',
        'date_of_birth',
        'age_display'
    ]
    list_filter = ['date_of_birth']
    search_fields = ['student__first_name', 'student__last_name', 'email', 'phone']

    def student_display(self, obj):
        if hasattr(obj, 'student'):
            return format_html(
                '<a href="/admin/study/student/{}/change/">{}</a>',
                obj.student.id,
                obj.student.full_name
            )
        return "Нет студента"
    student_display.short_description = 'Студент'

    def age_display(self, obj):
        from datetime import date
        if obj.date_of_birth:
            today = date.today()
            age = today.year - obj.date_of_birth.year - (
                    (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
            return f"{age} лет"
        return "-"
    age_display.short_description = 'Возраст'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student')