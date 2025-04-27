from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Habit
from .paginators import HabitListPagination
from .serializers import HabitSerializer


class HabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitListPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user).order_by("action")


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("action")


class HabitCreateView(generics.CreateAPIView):
    serializer_class = HabitSerializer


class HabitUpdateView(generics.UpdateAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения этой привычки.")
        return obj


class HabitDeleteView(generics.DestroyAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этой привычки.")
        return obj
