from django.contrib import admin

# Register your models here.
from .models import AbonnementClient

@admin.register(AbonnementClient)
class ProductOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'start_date', 'end_date', 'blocking_date',  'type_abonnement', 'presence_quantity')
    list_display_links = ('id','client',)
    search_fields = ('id', 'type_abonnement','client')
