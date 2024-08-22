from django.contrib import admin
from .models import  Creneau,Event


admin.site.register(Creneau)
admin.site.register(Event)
# from .models import Event
# from datetime import datetime

# Event.objects.create(title="Sample Event", start_time=datetime(2024, 8, 22, 10, 0), end_time=datetime(2024, 8, 22, 12, 0))