"""URL configuration for commissions app."""

from django.urls import path
from .views import CommissionDetailView, CommissionListView

urlpatterns = [
    path("requests/list", CommissionListView.as_view(), name="commission_detail"),
    path("request/<int:pk>", CommissionDetailView.as_view(), name="commission_list"),
]
