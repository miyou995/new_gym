from django.contrib import admin

# Register your models here.
from .models import Client
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.widgets import DateWidget
from import_export.fields import Field

@admin.register(Client)
class PersonAdmin(ImportExportModelAdmin):
    birth_date = Field(attribute='birth_date', column_name='<birth_date>', widget=DateWidget('%d/%m/%Y')) 
    date_added = Field(attribute='date_added', column_name='<date_added>', widget=DateWidget('%d/%m/%Y')) 
    pass

# class EmployeeResource(resources.ModelResource):
#     birth_date = Field(attribute='birth_date', column_name='<birth_date>', widget=DateWidget('<date_format>')) 
#     date_added = Field(attribute='date_added', column_name='<date_added>', widget=DateWidget('<date_format>')) 
#     class Meta:
#         model = Client
#         # fields = ('start_date',...)