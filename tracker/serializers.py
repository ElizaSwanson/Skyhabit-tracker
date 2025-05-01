from rest_framework import serializers

from .models import Habit
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["owner"]
        validators = [HabitValidator()]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
