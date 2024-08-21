
# from django.contrib import admin
# from django.db import models
# from .models import  User 
# from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.contrib.admin.views.main import ChangeList
# from django.urls import reverse
# from django.utils.safestring import mark_safe 
# from django.contrib.auth.models import Group
# # from django.contrib.sites.models import Site
# admin.site.unregister(Group)
# # admin.site.unregister(Site)
# class UserAdmin(DjangoUserAdmin):
#     fieldsets = (
#         (None, {"fields": ( "email", "magasin","password")}),
#         (
#                 "Personal info",
#                 {"fields": ("picture","pseudo", "role", "notes")},
#         ),
#         (
#                 "Permissions",
#                 {
#                   "fields":(
#                             "is_active",
#                             "is_staff",
#                             "is_manager",
#                             "is_superuser",
#                             "user_permissions",
#          )
#                 },
#                 ),
#                 (
#                 "Important dates",
#                 {"fields": ("last_login", "date_joined")},
#                 ),
#                 )
#     add_fieldsets = (
#                 (
#                 None,
#                 {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#                 },
#                 ),
#                 )

#     list_display = (
#                 "id",
#                 "email",
                
#                 "role",
#                 "warehouse",
#                 "is_staff",
#                 "is_active"
#                 )
#     search_fields = ("email", "picture", "role" )
#     ordering = ("email"),
  


# admin.site.register(User, UserAdmin) 


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
