from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User

from habits.tasks import check_habits_and_notify
from freezegun import freeze_time
from unittest.mock import patch

class HabitTest(APITestCase):
    """
    Тестирование API для модели Habit
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.habit = Habit.objects.create(
            action="test полезная привычка",
            place="test место",
            time="12:00",
            reward="test вознаграждение",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_habit(self):
        """
        Тест получения списка привычек
        """
        url = reverse("habits:habit-list")
        response = self.client.get(url)

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "time_to_complete": "00:02:00",
                    "period": 1,
                    "action": "test полезная привычка",
                    "place": "test место",
                    "time": "12:00:00",
                    "is_enjoyable_habit": False,
                    "reward": "test вознаграждение",
                    "is_published": True,
                    "related_habit": None,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)

    def test_create_habit(self):
        """
        Тест создания привычки
        """
        url = reverse("habits:habit-list")
        data = {
            "action": "test1 полезная привычка",
            "place": "test1 место",
            "reward": "test1 вознаграждение",
            "time": "12:00:00",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_retrieve_habit(self):
        """
        Получение конкретной привычки
        """
        url = reverse("habits:habit-detail", kwargs={"pk": self.habit.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["action"], "test полезная привычка")

    def test_update_habit(self):
        """
        Тест на изменения привычке
        """
        url = reverse("habits:habit-detail", args=(self.habit.pk,))

        data = {"action": "test1 полезная привычка", "reward": "test вознаграждение"}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["action"],
            "test1 полезная привычка",
        )

    def test_delete_habit(self):
        """
        удаления привычки
        """
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_publish_habits_list(self):
        """
        получения списка публичных привычек
        """
        url = reverse("habits:publish_habits")

        response = self.client.get(url)

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.id,
                    "time_to_complete": "00:02:00",
                    "period": 1,
                    "action": "test полезная привычка",
                    "place": "test место",
                    "time": "12:00:00",
                    "is_enjoyable_habit": False,
                    "reward": "test вознаграждение",
                    "is_published": True,
                    "related_habit": None,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)

    @patch('habits.tasks.send_telegram_message')
    def test_check_habits_and_notify_sends_message(self, mock_send):
        """Отправляет сообщение, если до привычки осталось 2 минуты"""
        with freeze_time("2026-04-26 12:00:00"):
            user = User.objects.create(email="telegram_user@test.ru", chat_id=123456789)
            habit = Habit.objects.create(
                action="Пробежка",
                place="Парк",
                time="12:02",
                owner=user,
                reward="Отдых"
            )
            check_habits_and_notify()
            mock_send.assert_called_once()
            args, _ = mock_send.call_args
            self.assertIn("Пробежка", args[0])
            self.assertEqual(args[1], str(user.chat_id))

    @patch('habits.tasks.send_telegram_message')
    def test_check_habits_and_notify_no_send(self, mock_send):
        """Не отправляет, если до привычки больше 5 минут"""
        with freeze_time("2026-04-26 12:00:00"):
            user = User.objects.create(email="telegram_user2@test.ru", chat_id=987654321)
            habit = Habit.objects.create(
                action="Чтение",
                place="Дом",
                time="12:10",
                owner=user,
                reward="Кофе"
            )
            check_habits_and_notify()
            mock_send.assert_not_called()