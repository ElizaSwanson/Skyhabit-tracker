from django.db import models
from rest_framework.exceptions import ValidationError

from config import settings


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )
    location = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Место выполнения"
    )
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )
    time_to_complete = models.PositiveIntegerField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(default=True, verbose_name="Признак публичности")

    def __str__(self):
        return self.action

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя совмещать вознаграждение и связанную привычку."
            )
        if self.time_to_complete > 120:
            raise ValidationError("Время выполнения не должно быть больше 120 минут.")
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Периодичность выполнения должна быть от 1 до 7 дней")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
