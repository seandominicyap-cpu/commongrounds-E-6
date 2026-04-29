"""URL configuration for commissions app."""

from django.urls import path, include
from .views import AccountUpdateView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('<str:username>/', AccountUpdateView.as_view(), name='accounts_update'),
]
