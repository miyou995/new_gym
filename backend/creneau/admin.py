from django.contrib import admin

from .models import Creneau

# admin.site.register(Event)
# @admin.register(Creneau)
# class CreaneauAdmin(admin.ModelAdmin):
#     list_display = ('id','name', 'hour_start', 'hour_finish', 'planning', 'activity')

# from .models import Event
# from datetime import datetime

# Event.objects.create(title="Sample Event", start_time=datetime(2024, 8, 22, 10, 0), end_time=datetime(2024, 8, 22, 12, 0))


@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hour_start", "hour_finish", "planning", "activity")
    search_fields = ("name", "planning__name", "activity__name")
    list_filter = ("planning", "activity", "hour_start")
