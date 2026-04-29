"""URL configuration for commissions app."""

from django.urls import path
from .views import AccountUpdateView

urlpatterns = [
    path("<int:pk>/edit/", AccountUpdateView.as_view(), name="accounts_update"),
]
