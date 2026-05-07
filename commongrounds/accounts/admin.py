from django.contrib import admin
from .models import Profile, Role


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
