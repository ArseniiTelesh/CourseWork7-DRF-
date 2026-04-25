from datetime import timedelta

from rest_framework.exceptions import ValidationError


class RelatedEnjoyableOrRewardValidator:

    def __init__(self, reward, related_habit, is_enjoyable_habit):
        self.reward = reward
        self.related_habit = related_habit
        self.is_enjoyable_habit = is_enjoyable_habit

    def __call__(self, value):
        reward_field = value.get(self.reward)
        related_habit_field = value.get(self.related_habit)
        is_enjoyable_habit_field = value.get(self.is_enjoyable_habit)

        if reward_field and related_habit_field:
            raise ValidationError(
                "Нельзя одновременно указать и связанную привычку, и вознаграждение. "
                "Выберите что-то одно."
            )

        if is_enjoyable_habit_field and (reward_field or related_habit_field):
            raise ValidationError(
                "У приятной привычки не может быть награды или связанной привычки"
            )

        if related_habit_field:
            if not related_habit_field.is_enjoyable_habit:
                raise ValidationError("Связанная привычка должна быть приятной")


def execution_time_validator(value):
    """
    Валидатор для проверки продолжительности выполнения привычки не более 120 секунд
    """
    if value:
        if value > timedelta(seconds=120):
            raise ValidationError(
                "Продолжительность выполнения привычки не может быть более 120 секунд"
            )


def execution_period_validator(value):
    """
    Валидатор для проверки продолжительности выполнения привычки не более 120 секунд
    """
    if value:
        if value > 7:
            raise ValidationError(
                "Продолжительность выполнения привычки не может реже 1 раза в 7 дней (реже раза в неделю)"
            )
