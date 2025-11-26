from django.http import HttpResponse
from django.shortcuts import render
import logging

# Получаем логгер
logger = logging.getLogger('app')

def log(request):
    logger.debug('Это сообщение уровня DEBUG')
    logger.info('Пользователь зашел на страницу')
    logger.warning('Необычная ситуация')
    logger.error('Произошла ошибка')
    logger.critical('Критическая ошибка!')

    # Логируем все GET параметры
    logger.info(
        "GET параметры запроса: %s",
        dict(request.GET)
    )

    return HttpResponse("OK")
