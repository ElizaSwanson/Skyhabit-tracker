from django.urls import path

from .apps import TrackerConfig
from .views import (HabitCreateView, HabitDeleteView, HabitListView,
                    HabitUpdateView, PublicHabitListView)

app_name = TrackerConfig.name

urlpatterns = [
    path(
        "list/", HabitListView.as_view(), name="habit-list"
    ),
    path(
        "list/public/", PublicHabitListView.as_view(), name="habit-list-public"
    ),
    path(
        "create/", HabitCreateView.as_view(), name="habit-create"
    ),
    path(
        "edit/<int:pk>/", HabitUpdateView.as_view(), name="habit-update"
    ),
    path(
        "delete/<int:pk>/", HabitDeleteView.as_view(), name="habit-delete"
    ),
]
