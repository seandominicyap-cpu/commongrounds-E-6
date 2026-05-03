from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BookReview, Bookmark, Borrow
from .forms import BookFormFactory, BorrowForm

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    ctx = {"books": books}

    if request.user.is_authenticated:
        profile = request.user.profile
        contributed = Book.objects.filter(contributor=profile)
        bookmarked = Book.objects.filter(bookmark__profile=profile)
        reviewed = Book.objects.filter(bookreview__user_reviewer=profile)

        user_books = books.exclude(contributor=profile).exclude(
            bookmark__profile=profile).exclude(bookreview__user_reviewer=profile)

        ctx["books"] = books.exclude(id__in=user_books)
        ctx["contributed_books"] = contributed
        ctx["bookmarked_books"] = bookmarked
        ctx["reviewed_books"] = reviewed

    return render(request, "bookclub/book_list.html", ctx)


def book_detail(request, id):
    book = Book.objects.all()
    ReviewForm = BookFormFactory.get_form('review')
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if request.user.is_authenticated:
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = "Anonymous"
            review.save()
            return redirect("bookclub:book_detail", id=book.id)
    ctx = {
        "book": book,
        "review_form": form,
        "reviews": BookReview.objects.filter(book=book),
        "bookmark_count": Bookmark.objects.filter(book=book).count(),
        "already_bookmarked": Bookmark.objects.filter(profile=request.user.profile, book=book).exists() if request.user.is_authenticated else False,
    }

    return render(request, "bookclub/book_detail.html", ctx)


@login_required
@role_required(["Book Contributor"])
def book_create(request):
    ContributeForm = BookFormFactory.get_form('contribute')
    form = ContributeForm()

    if request.method == "POST":
        form = ContributeForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect("bookclub:book_detail", id=book.id)
    ctx = {"form": form}
    return render(request, "bookclub/book_form.html", ctx)


@login_required
@role_required(["Book Contributor"])
def book_update(request, id):
    book = Book.objects.get(id=id)
    UpdateForm = BookFormFactory.get_form('update')
    form = UpdateForm(instance=book)

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("bookclub:book_detail", id=book.id)

    ctx = {"form": form, "book": book}
    return render(request, "bookclub/book_form.html", ctx)


def book_borrow(request, id):
    book = Book.objects.get(id=id)
    form = BorrowForm()

    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book
            if request.user.is_authenticated:
                borrow.borrower = request.user.profile
                borrow.name = request.user.profile.display_name
            else:
                borrow.name = request.POST.get("name", "")

            borrow.date_to_return = borrow.date_borrowed + timedelta(weeks=2)
            borrow.save()
            return redirect("bookclub:book_detail", id=book.id)
    ctx = {"form": form, "book": book}
    return render(request, "bookclub/book_borrow.html", ctx)


@login_required
def book_bookmark(request, id):
    book = Book.objects.get(id=id)
    bookmark = Bookmark.objects.filter(profile=request.user.profile, book=book)

    if bookmark.exists():
        bookmark.delete()

    else:
        Bookmark.objects.create(profile=request.user.profile, book=book)

    return redirect("bookclub:book_detail", id=book.id)
