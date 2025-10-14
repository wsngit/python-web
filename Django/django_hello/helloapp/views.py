from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def hello_world(request):
    # Простейший вариант - возвращаем текст
    return HttpResponse("Hello, World!")

@csrf_exempt
def request_info(request):
    meta_data = {}
    for key, value in request.META.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            meta_data[key] = value


    return JsonResponse({
        'headers from META': meta_data,
        'headers': dict(request.headers),
        'GET params': request.GET,
        #'POST params - form-data': request.POST,
        'POST params - body': str(request.body),
    })

