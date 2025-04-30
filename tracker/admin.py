from django.contrib import admin

from tracker.models import Habit
from users.models import User

admin.site.register(User)
admin.site.register(Habit)
