from django.urls import path

from . import views

app_name = "bookclub"

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("book/<int:id>/", views.book_detail, name="book_detail"),
    path("book/add/", views.book_create, name="book_create"),
    path("book/<int:id>/edit/", views.book_update, name="book_update"),
    path("book/<int:id>/borrow/", views.book_borrow, name="book_borrow"),
    path("book/<int:id>/bookmark/", views.book_bookmark, name="book_bookmark"),
]
