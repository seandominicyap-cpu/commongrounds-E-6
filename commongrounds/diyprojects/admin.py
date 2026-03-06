from django.contrib import admin
from .models import Project, ProjectCategory
from django.contrib.auth.models import User

# Register your models here.

class ProjectCategoryInLine(admin.TabularInline):
    model = ProjectCategory
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectCategoryInLine]
    list_display = ('title', 'category', 'description', 'materials', 'steps', 'created_on', 'updated_on')

admin.site.register(User)
admin.site.register(ProjectCategory)
admin.site.register(Project, ProjectAdmin)
# Register your models here.
