from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Habit


User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_habit_creation(self):
        habit = Habit.objects.create(
            owner=self.user,
            location="Дом",
            time="00:00:00",
            action="Попить пива",
            is_pleasant=True,
            frequency=1,
            reward="Можно расслабиться",
            time_to_complete=60,
            is_public=True,
        )
        self.assertIsInstance(habit, Habit)
        self.assertEqual(habit.action, "Попить пива")
        self.assertEqual(habit.location, "Дом")
        self.assertEqual(habit.frequency, 1)

    def test_habit_string_representation(self):
        habit = Habit.objects.create(
            owner=self.user,
            location="Дом",
            time="00:00:00",
            action="Попить пива",
            is_pleasant=True,
            frequency=1,
            reward="Можно расслабиться",
            time_to_complete=60,
            is_public=True,
        )
        self.assertEqual(str(habit), habit.action)


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.valid_habit_data = {
            "location": "Дом",
            "time": "10:00:00",
            "action": "Попить пива",
            "is_pleasant": True,
            "frequency": 1,
            "reward": None,
            "time_to_complete": 60,
            "is_public": True,
        }

    def test_invalid_habit_with_both_reward_and_related_habit(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["reward"] = "Ничего"
        invalid_data["related_habit"] = True

    def test_invalid_time_to_complete(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["time_to_complete"] = 121

    def test_invalid_frequency(self):
        invalid_data = self.valid_habit_data.copy()
        invalid_data["frequency"] = 8


class HabitAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            owner=self.user,
            location="Дом",
            time="00:00:00",
            action="Пойти спать",
            is_pleasant=True,
            frequency=1,
            reward=None,
            time_to_complete=60,
            is_public=True,
        )

    def test_create_habit(self):
        response = self.client.post(
            "/tracker/create/",
            {
                "location": "Дом",
                "time": "10:00:00",
                "action": "Попить пива",
                "is_pleasant": False,
                "frequency": 1,
                "reward": "Пиво",
                "time_to_complete": 60,
                "is_public": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Попить пива")

    def test_update_habit(self):
        response = self.client.patch(
            f"/tracker/edit/{self.habit.id}/",
            {
                "location": "Дом",
                "time": "10:00:00",
                "action": "Побегать",
                "is_pleasant": False,
                "frequency": 1,
                "reward": "Пиво",
                "time_to_complete": 60,
                "is_public": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Побегать")
        self.assertEqual(self.habit.frequency, 1)

    def test_delete_habit(self):
        response = self.client.delete(f"/tracker/delete/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_list_user_habits(self):
        response = self.client.get("/tracker/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_public_habits(self):
        public_habit = Habit.objects.create(
            owner=self.user,
            location="Парк",
            time="20:00:00",
            action="Пробежка",
            is_pleasant=False,
            frequency=1,
            reward="Еда",
            time_to_complete=30,
            is_public=True,
        )
        response = self.client.get("/tracker/list/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(public_habit.action, [habit["action"] for habit in response.data])
