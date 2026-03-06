from django.contrib import admin
from .models import Project, ProjectCategory

class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name")

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'description', 'materials', 'steps', 'created_on', 'updated_on')

admin.site.register(ProjectCategory)
admin.site.register(Project, ProjectAdmin)
