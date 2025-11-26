# tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)

def task():
    logger.info("Задача выполняется!")

def daily_task():
    logger.info("Ежедневная задача выполняется!")


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Добавляем задачи
    scheduler.add_job(
        task,
        'interval',
        seconds=5,
        id='task',
        replace_existing=True
    )

    # Еще пример - ежедневно в 8:00
    scheduler.add_job(
        daily_task,
        'cron',
        hour=8,
        minute=0,
        id='daily_task',
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started!")