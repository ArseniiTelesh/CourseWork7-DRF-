from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, HabitPublishListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register("habit", HabitViewSet, basename="habit")

urlpatterns = [
    path("publish_habits/", HabitPublishListAPIView.as_view(), name="publish_habits")
] + router.urls
