from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


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
                    "id": 5,
                    "time_to_complete": "00:02:00",
                    "period": 1,
                    "action": "test полезная привычка",
                    "place": "test место",
                    "time": "12:00:00",
                    "is_enjoyable_habit": False,
                    "reward": "test вознаграждение",
                    "is_published": True,
                    "related_habit": None,
                    "owner": 4,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)
