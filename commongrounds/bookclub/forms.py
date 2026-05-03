from django import forms
from .models import Book, BookReview, Borrow


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReviewfields = ['title', 'comment']


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow'
        ]
        widgets = {
            'genre': forms.Select(),
        }


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow'
        ]
        widgets = {
            'genre': forms.Select(),
        }


class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['date_borrowed']
        widgets = {
            'date_borrowed': forms.DateInput(attrs={'type': 'date'}),
        }


class BookFormFactory:
    @classmethod
    def get_form(cls, context):
        if context == 'review':
            return BookReviewForm
        elif context == 'contribute':
            return BookContributeForm
        elif context == 'update':
            return BookUpdateForm
        else:
            raise ValueError(f"Unknown form context: {context}")
