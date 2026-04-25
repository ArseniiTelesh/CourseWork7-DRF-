from datetime import datetime

from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    RelatedEnjoyableOrRewardValidator,
    execution_time_validator,
    execution_period_validator,
)


class HabitSerializer(serializers.ModelSerializer):

    time_to_complete = serializers.DurationField(
        validators=[execution_time_validator], required=False
    )
    period = serializers.IntegerField(
        validators=[execution_period_validator], required=False
    )

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = [
            "owner",
        ]

        validators = [
            RelatedEnjoyableOrRewardValidator(
                "reward",
                "related_habit",
                "is_enjoyable_habit",
            ),
        ]

    def create(self, validated_data):
        """Если время не передано - ставим текущее (без секунд)"""
        if "time" not in validated_data or validated_data["time"] is None:
            now = datetime.now()
            validated_data["time"] = now.replace(second=0, microsecond=0).time()
        return super().create(validated_data)
