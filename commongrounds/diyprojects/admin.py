from django.contrib import admin
from .models import Project, ProjectCategory, Profile, Favorite, ProjectReview, ProjectRating
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category')
    search_fields = ('title', 'description')
    list_filter = ('category', 'creator')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('profile', 'project')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'reviewer', 'review_text')

class RatingAdmin(admin.ModelAdmin):
    list_display = ('project', 'score')
    list_filter = ('score',)

admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(Favorite)
admin.site.register(ProjectReview)
admin.site.register(ProjectRating)