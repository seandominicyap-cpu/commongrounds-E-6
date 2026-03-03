"""
URL configuration for commissions app
"""
from django.contrib import admin
from django.urls import path
from .views import CommissionDetailView, CommissionListView
urlpatterns = [
    path('requests', CommissionDetailView.as_view(), name="commission_detail"),
    path('request/<int:pk>', CommissionListView.as_view(), name="commission_list"),
]
