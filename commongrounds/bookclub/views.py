from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BookReview, Bookmark, Borrow
from .forms import BookFormFactory, BorrowForm

# Create your views here.


def book_list(request):
    books = Book.objects.all()

    if request.user.is_authenticated:
        profile = request.user.profile
        contributed = Book.objects.filter(contributor=profile)
        bookmarked = Book.objects.filter(bookmark__profile=profile)
        reviewed = Book.objects.filter(bookreview__user_reviewer=profile)

        user_books = all_books.exclude(contributor=profile).exclude(
            bookmark__profile=profile).exclude(bookreview__user_reviewer=profile)

        ctx["books"] = books.exclude(id__in=user_books)
        ctx["contributed_books"] = contributed
        ctx["bookmarked_books"] = bookmarked
        ctx["reviewed_books"] = reviewed

    return render(request, "bookclub/book_list.html", ctx)


def book_detail(request, id):
    books = Book.objects.all()

    return render(request, "bookclub/book_detail.html", ctx)


def book_create(request, id):


def book_update(request, id):


def book_borrow(request, id):
