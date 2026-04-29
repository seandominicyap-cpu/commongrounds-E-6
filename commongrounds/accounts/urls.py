"""URL configuration for commissions app."""

from django.urls import path
from .views import AccountUpdateView

urlpatterns = [
    path("<str:username>/", AccountUpdateView.as_view(), name="accounts_update"),
]
