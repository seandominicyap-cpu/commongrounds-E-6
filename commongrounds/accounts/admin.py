from django.contrib import admin
from .models import Profile, Role


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)
