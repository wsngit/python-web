from django.db import models

class Course(models.Model):
    """Модель курса"""
    name = models.CharField(max_length=100, verbose_name='Название курса')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код курса')
    description = models.TextField(blank=True, verbose_name='Описание')


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Group(models.Model):
    """Модель группы"""
    name = models.CharField(max_length=50, verbose_name='Название группы')
    code = models.CharField(max_length=20, unique=True, verbose_name='Код группы')
    courses = models.ManyToManyField(
        Course,
        related_name='groups',
        verbose_name='Курсы',
        blank=True
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        course_names = ", ".join([course.name for course in self.courses.all()])
        return f"{self.name} - {course_names}" if course_names else f"{self.name}"

    @property
    def student_count(self):
        """Количество студентов в группе"""
        return self.students.count()

class StudentInfo(models.Model):
    """Дополнительная информация о студенте"""
    address = models.TextField(blank=True, verbose_name='Адрес')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    date_of_birth = models.DateField(verbose_name='Дата рождения')

    student = models.OneToOneField(
        'Student',
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name='Студент'
    )

    class Meta:
        verbose_name = 'Информация о студенте'
        verbose_name_plural = 'Информация о студентах'

    def __str__(self):
        return f"Информация: {self.email}"

class Student(models.Model):
    """Модель студента"""
    # Основная информация
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='ID студента'
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    # Связь с группой
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Группа'
    )

    # Системные поля
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.student_id})"

    @property
    def full_name(self):
        """Полное имя студента"""
        return f"{self.last_name} {self.first_name}"