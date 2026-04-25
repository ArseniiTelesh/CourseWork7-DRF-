from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как владельца
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitPublishListAPIView(ListAPIView):
    """Класс контроллера для списка публичных привычек"""

    queryset = Habit.objects.filter(is_published=True)

    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPaginator
