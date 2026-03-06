from django.shortcuts import render
from .models import Book

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    ctx = {"books": books}

    return render(request, "bookclub/book_list.html", ctx)


def book_detail(request, id):
    ctx = {"book": Book.objects.get(id=id)}

    return render(request, "bookclub/book_detail.html", ctx)
