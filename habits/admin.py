from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка модели Habit
    """

    list_display = (
        "id",
        "action",
        "is_enjoyable_habit",
        "related_habit",
        "reward",
        "is_published",
    )
    list_filter = ("is_enjoyable_habit",)
    search_fields = ("action",)
