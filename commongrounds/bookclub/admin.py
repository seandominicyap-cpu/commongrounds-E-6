from django.contrib import admin
from .models import Book, Genre

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
