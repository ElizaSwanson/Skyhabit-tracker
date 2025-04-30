import requests
from celery import shared_task

from config import settings

from .models import Habit


@shared_task
def send_reminder():

    for habit in Habit.objects.all():
        message = (
            f"Не забудьте выполнить привычку: {habit.action}\n"
            f"Время выполнения: {habit.time}\n"
            f"Место выполнения: {habit.location}."
        )
        params = {
            "text": message,
            "chat_id": habit.telegram_chat_id,
        }

        requests.post(
            f"http://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            params=params,
        )
