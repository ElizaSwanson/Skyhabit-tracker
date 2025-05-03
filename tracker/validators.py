from rest_framework import serializers

from .models import Habit


class HabitValidator:

    def validate_related_habit(self, attrs):
        if attrs.get("related_habit_id"):
            related_habit = Habit.objects.get(pk=attrs.get("related_habit_id"))
            if not related_habit.is_pleasant:
                raise serializers.ValidationError("Можно выбрать только хорошую привычку")

    def validate_reward(self, attrs):
        """Validates that only reward or a related habit are selected in the same time."""
        if attrs.get("related_habit_id") and attrs.get("reward"):
            raise serializers.ValidationError(
                "Или награда, или выполнение хорошей привычки!"
            )

    def validate_pleasant_habit(self, attrs):
        if attrs.get("is_pleasant") and any(
            [attrs.get("related_habit_id"), attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]
        ):
            raise serializers.ValidationError(
                "Или награда, или выполнение хорошей привычки!!!"
            )
        if not attrs.get("is_pleasant") and not any(
            [
                all([attrs.get("reward"), attrs.get("frequency"), attrs.get("time")]),
                all([attrs.get("related_habit_id"), attrs.get("frequency"), attrs.get("time")]),
            ]
        ):
            raise serializers.ValidationError(
                "Выберите или награду, или выполнение хорошей привычки"
            )

    def __call__(self, attrs):
        self.validate_related_habit(attrs)
        self.validate_reward(attrs)
        self.validate_pleasant_habit(attrs)
