# app/management/commands/scheduled_task.py
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging

logger = logging.getLogger('app')

class Command(BaseCommand):
    help = 'Задача по расписанию'

    def handle(self, *args, **options):
        logger.info(f'Задача выполняется в {timezone.now()}')
