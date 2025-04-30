from django.urls import path

from .apps import TrackerConfig
from .views import (HabitCreateView, HabitDeleteView, HabitListView,
                    HabitUpdateView, PublicHabitListView)

app_name = TrackerConfig.name

urlpatterns = [
    path("list/", HabitListView.as_view(), name="tracker-list"),
    path("list/public/", PublicHabitListView.as_view(), name="tracker-list-public"),
    path("create/", HabitCreateView.as_view(), name="tracker-create"),
    path("edit/<int:pk>/", HabitUpdateView.as_view(), name="tracker-update"),
    path("delete/<int:pk>/", HabitDeleteView.as_view(), name="tracker-delete"),
]
