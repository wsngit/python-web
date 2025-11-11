import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .forms import PythonSyntaxTestForm

def home(request):
    return render(request, 'hello.html', )

def python_test_view(request):
    # Правильные ответы
    correct_answers = {
        'question_1': '#',
        'question_2': 'list',
        'question_3': 'def',
        'question_4': ['indentation'],  # Только отступы
        'question_5': {"name": "value", "age": "value"},  # Пример правильного формата
        'question_6': 5,
        'question_7': False,  # Строки НЕ изменяемы
    }

    if request.method == 'POST':
        form = PythonSyntaxTestForm(request.POST)
        if form.is_valid():
            # Проверка ответов
            score = 0
            user_answers = form.cleaned_data
            results = {}

            # Вопрос 1
            if user_answers['question_1'].strip() == correct_answers['question_1']:
                score += 1
                results['question_1'] = True
            else:
                results['question_1'] = False

            # Вопрос 2
            if user_answers['question_2'] == correct_answers['question_2']:
                score += 1
                results['question_2'] = True
            else:
                results['question_2'] = False

            # Вопрос 3
            if user_answers['question_3'] == correct_answers['question_3']:
                score += 1
                results['question_3'] = True
            else:
                results['question_3'] = False

            # Вопрос 4
            if set(user_answers['question_4']) == set(correct_answers['question_4']):
                score += 1
                results['question_4'] = True
            else:
                results['question_4'] = False

            # Вопрос 5 - проверяем только синтаксис словаря
            try:
                user_dict = eval(user_answers['question_5'])
                if isinstance(user_dict, dict) and 'name' in user_dict and 'age' in user_dict:
                    score += 1
                    results['question_5'] = True
                else:
                    results['question_5'] = False
            except:
                results['question_5'] = False

            # Вопрос 6
            if user_answers['question_6'] == correct_answers['question_6']:
                score += 1
                results['question_6'] = True
            else:
                results['question_6'] = False

            # Вопрос 7
            if user_answers['question_7'] == correct_answers['question_7']:
                score += 1
                results['question_7'] = True
            else:
                results['question_7'] = False

            # Подготовка данных для отображения результатов
            context = {
                'score': score,
                'total': 7,
                'percentage': int((score / 7) * 100),
                'results': results,
                'user_answers': user_answers,
                'correct_answers': correct_answers,
            }

            return render(request, 'test_results.html', context)

    else:
        form = PythonSyntaxTestForm()

    return render(request, 'test.html', {'form': form})

def get_uploaded_images():
    """Получаем список всех изображений в папке uploads"""
    uploads_dir = settings.UPLOADS_DIR
    images = []

    if uploads_dir.exists():
        for filename in os.listdir(uploads_dir):
            file_path = uploads_dir / filename
            if file_path.is_file() and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                stat = file_path.stat()
                images.append({
                    'filename': filename,
                    'url': f"{settings.MEDIA_URL}uploads/{filename}",
                    'uploaded_time': stat.st_mtime,
                    'size': stat.st_size,
                    'path': file_path
                })

    # Сортируем по времени загрузки (новые сначала)
    images.sort(key=lambda x: x['uploaded_time'], reverse=True)
    return images

def simple_gallery_view(request):
    """Простая галерея"""
    images = get_uploaded_images()

    if request.method == 'POST':
        # Простая валидация
        image_file = request.FILES.get('image')
        title = request.POST.get('title', '').strip()

        if not image_file:
            messages.error(request, 'Выберите файл для загрузки')
        else:
            # Проверка размера
            if image_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Файл слишком большой (макс. 5MB)')
            else:
                # Проверка формата
                valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
                ext = os.path.splitext(image_file.name)[1].lower()
                if ext not in valid_extensions:
                    messages.error(request, f'Неподдерживаемый формат. Используйте: {", ".join(valid_extensions)}')
                else:
                    # Сохраняем файл
                    if title:
                        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        filename = f"{safe_title}{ext}"
                    else:
                        filename = image_file.name

                    fs = FileSystemStorage(location=settings.UPLOADS_DIR)
                    filename = fs.get_available_name(filename)
                    fs.save(filename, image_file)

                    messages.success(request, f'Изображение "{filename}" успешно загружено!')
                    return redirect('gallery')

    return render(request, 'gallery.html', {
        'images': images,
        'total_images': len(images)
    })

def delete_image(request, filename):
    """Удаление изображения"""
    if request.method == 'POST':
        file_path = settings.UPLOADS_DIR / filename

        if file_path.exists():
            file_path.unlink()
            messages.success(request, f'Изображение "{filename}" удалено')
        else:
            messages.error(request, 'Файл не найден')

    return redirect('gallery')

def clear_gallery(request):
    """Очистка всей галереи"""
    if request.method == 'POST':
        images = get_uploaded_images()
        deleted_count = 0

        for image in images:
            try:
                image['path'].unlink()
                deleted_count += 1
            except:
                continue

        messages.success(request, f'Удалено {deleted_count} изображений')

    return redirect('gallery')
