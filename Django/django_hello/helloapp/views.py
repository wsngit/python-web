from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    # Простейший вариант - возвращаем текст
    return HttpResponse("Hello, World!")