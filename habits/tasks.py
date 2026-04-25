from datetime import timedelta, datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def check_habits_and_notify():
    now = datetime.now()
    habits = Habit.objects.filter(owner__chat_id__isnull=False)
    for habit in habits:
        habit_datetime = datetime.combine(now.date(), habit.time)
        time_left = habit_datetime - now  # сколько осталось до выполнения

        # Если осталось от 0 до 5 минут (включительно)
        if habit.owner.chat_id and timedelta(0) <= time_left <= timedelta(minutes=5):
            text = f"мне нужно {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"
            send_telegram_message(text, habit.owner.chat_id)
