from datetime import timedelta

from django.db import models

NULLABLE = {"null": True, "blank": True}


class Habit(models.Model):
    """
    Модель привычки
    """

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="владелец (пользователь)"
    )
    place = models.CharField(
        max_length=300, verbose_name="место, в котором необходимо выполнять привычку"
    )
    time = models.TimeField(verbose_name="время, когда необходимо выполнять привычку")
    action = models.CharField(
        max_length=300, verbose_name="действие, которое представляет собой привычка"
    )
    is_enjoyable_habit = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, verbose_name="Связанная привычка", **NULLABLE
    )
    period = models.IntegerField(
        verbose_name="Периодичность привычки (в днях)",
        default=1,
        help_text="Периодичность в днях",
    )
    reward = models.CharField(verbose_name="Вознаграждение за привычку", **NULLABLE)
    time_to_complete = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name="Продолжительность выполнения привычки по времени",
    )
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def __str__(self):
        return self.action
