from django.shortcuts import render
import os
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES.get('image')

            if not uploaded_file:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Файл не предоставлен'
                }, status=400)

            # Проверка размера файла (5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Файл слишком большой (макс. 5MB)'
                }, status=400)

            # Проверка типа файла
            allowed_types = ['image/jpeg', 'image/png']
            if uploaded_file.content_type not in allowed_types:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Недопустимый тип файла'
                }, status=400)

            # Сохранение файла
            fs = FileSystemStorage(location='uploads')
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(f"files/uploads/{filename}")

            return JsonResponse({
                'status': 'success',
                'message': 'Файл успешно загружен',
                'file_name': filename,
                'file_url': file_url,
                'file_size': uploaded_file.size
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Только POST запросы'
    }, status=405)

def get_file(request, filename):
    """Возвращает изображение по имени файла"""
    file_path = os.path.join('uploads', filename)

    if not os.path.exists(file_path):
        return HttpResponse('File not found', status=404)

    return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
