"""URL configuration for commissions app."""

from django.urls import path, include
from .views import AccountUpdateView, RegisterView, DashboardView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('<str:username>/', AccountUpdateView.as_view(), name='accounts_update'),
    path('<str:username>/dashboard', DashboardView.as_view(), name='dashboard'),
]
