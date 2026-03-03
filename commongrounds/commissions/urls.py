"""
URL configuration for commissions app
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('commissions/requests', admin.site.urls),
    path('commissions/request/<int:pk>', admin.site.urls),
]
