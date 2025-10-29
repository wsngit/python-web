from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Group, Student
from .forms import CourseForm

def index(request):
    return render(request, "index.html")

def request(request):
    return render(request, "request.html")

def course_create(request):
    """
    Представление для создания нового курса
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()

    context = {
        'form': form,
        'title': 'Создание нового курса'
    }
    return render(request, 'course_form.html', context)

def course_detail(request, course_id):
    """
    Представление детальной информации о курсе
    """
    # Получаем курс или возвращаем 404
    course = get_object_or_404(Course, id=course_id)

    # Получаем группы, связанные с этим курсом
    groups = Group.objects.filter(courses=course).select_related()

    # Получаем студентов, которые в группах этого курса
    students_in_course = Student.objects.filter(
        group__courses=course,
        is_active=True
    ).select_related('group')

    # Подсчитываем статистику
    total_groups = groups.count()
    total_students = students_in_course.count()

    # Собираем данные для шаблона
    context = {
        'course': course,
        'total_groups': total_groups,
        'total_students': total_students,
    }

    # Рендерим шаблон
    return render(request, 'course_detail.html', context)

def course_list(request):
    """
    Представление списка курсов
    """
    # Получаем все курсы
    courses = Course.objects.all()

    # Подсчитываем статистику для каждого курса
    course_data = []
    for course in courses:
        groups_count = Group.objects.filter(courses=course).count()
        students_count = Student.objects.filter(
            group__courses=course,
            is_active=True
        ).count()

        course_data.append({
            'course': course,
            'groups_count': groups_count,
            'students_count': students_count,
        })

    context = {
        'course_data': course_data,
    }

    return render(request, 'course_list.html', context)

