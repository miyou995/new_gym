from django.contrib import admin

# Register your models here.
from .models import Salle
# Register your models here.


@admin.register(Salle)
class PlanningAdmin(admin.ModelAdmin):
    list_display =(
         'name',
        
        
    )