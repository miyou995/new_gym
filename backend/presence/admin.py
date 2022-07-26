from django.contrib import admin
from .models import  Presence
from client.models import Client
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

@admin.register(Presence)
class PresencenAdmin(ImportExportModelAdmin):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'id'))

