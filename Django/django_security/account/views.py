from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Успешная аутентификация')
                else:
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def user_profile_detailed(request):
    user = request.user

    # Основная информация о пользователе
    user_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name or 'Не указано',
        'last_name': user.last_name or 'Не указано',
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined.strftime('%d.%m.%Y %H:%M'),
        'last_login': user.last_login.strftime('%d.%m.%Y %H:%M') if user.last_login else 'Никогда',
    }

    # Группы пользователя
    user_groups = user.groups.all()

    # Все разрешения пользователя
    user_permissions = sorted(user.get_all_permissions())

    # Разрешения сгруппированные по приложениям
    permissions_by_app = {}
    for perm in user_permissions:
        app_label = perm.split('.')[0]
        if app_label not in permissions_by_app:
            permissions_by_app[app_label] = []
        permissions_by_app[app_label].append(perm)

    # Проверки системных разрешений
    permission_checks = {
        'auth.add_user': user.has_perm('auth.add_user'),
        'auth.change_user': user.has_perm('auth.change_user'),
        'auth.delete_user': user.has_perm('auth.delete_user'),
        'auth.view_user': user.has_perm('auth.view_user'),
        'admin.logentry_access': user.has_perm('admin.view_logentry'),
    }

    # Кастомные проверки
    custom_checks = {
        'Может управлять пользователями': user.has_perm('auth.add_user') and user.has_perm('auth.change_user'),
        'Имеет права администратора': user.is_staff or user.is_superuser,
        'Аутентифицирован': user.is_authenticated,
        'Активный аккаунт': user.is_active,
        'Может войти в админку': user.is_staff,
    }

    # Проверки для приложения (замените на свои)
    app_specific_checks = {
        'Может публиковать статьи': user.has_perm('blog.publish_article'),
        'Может модерировать комментарии': user.has_perm('blog.moderate_comment'),
        'Может просматривать отчеты': user.has_perm('blog.view_report'),
        'Может управлять контентом': user.has_perm('blog.change_article'),
    }

    # Информация о сессии
    session_info = {
        'Ключ сессии': request.session.session_key or 'Не создана',
        'Время жизни сессии': f"{request.session.get_expiry_age()} секунд",
        'Количество ключей в сессии': len(request.session.keys()),
    }

    # Статистика
    stats = {
        'groups_count': user_groups.count(),
        'permissions_count': len(user_permissions),
        'session_keys_count': len(request.session.keys()),
    }

    # Активные сессии (только для staff)
    if user.is_staff:
        from django.contrib.sessions.models import Session
        stats['active_sessions_count'] = Session.objects.filter(
            expire_date__gt=timezone.now()
        ).count()

    context = {
        'user': user,
        'user_info': user_info,
        'user_groups': user_groups,
        'user_permissions': user_permissions,
        'permissions_by_app': permissions_by_app,
        'permission_checks': permission_checks,
        'custom_checks': custom_checks,
        'app_specific_checks': app_specific_checks,
        'session_info': session_info,
        'stats': stats,
    }

    return render(request, 'account/user_profile_detailed.html', context)
