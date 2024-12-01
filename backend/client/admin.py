from django.contrib import admin

# Register your models here.
from .models import Client
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.widgets import DateWidget
from import_export.fields import Field

# @admin.register(Client)
# class PersonAdmin(ImportExportModelAdmin):
#     birth_date = Field(attribute='birth_date', column_name='<birth_date>', widget=DateWidget('%d/%m/%Y')) 
#     date_added = Field(attribute='date_added', column_name='<date_added>', widget=DateWidget('%d/%m/%Y')) 
#     pass

# class EmployeeResource(resources.ModelResource):
#     birth_date = Field(attribute='birth_date', column_name='<birth_date>', widget=DateWidget('<date_format>')) 
#     date_added = Field(attribute='date_added', column_name='<date_added>', widget=DateWidget('<date_format>')) 
#     class Meta:
#         model = Client
#         # fields = ('start_date',...)




from .models import  Client,Maladie,Personnel,Coach
from django.urls import path
from django.shortcuts import render, get_object_or_404

admin.site.register(Maladie)
admin.site.register(Personnel)
admin.site.register(Coach)

@admin.register(Client)
class clientAdmin(admin.ModelAdmin):
    list_display = (  "carte",
        "last_name",
        "first_name",
        "picture",
        "email",
        "adress",
        "phone",
        "civility",
        "birth_date",
        
       )
    search_fields = ("last_name", "first_name", "email")
    list_filter = ("civility", "birth_date")
    ordering = ("last_name", "first_name")
    readonly_fields = ("date_added",)
    list_display_links = ("carte", "last_name", "first_name")


  




