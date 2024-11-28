from django.contrib import admin
from .models import Planning
# Register your models here.


@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display =(
         'name',
        'salle_sport',
        
    )