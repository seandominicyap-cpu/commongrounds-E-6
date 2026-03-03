from django.urls import path

from .views import index

urlpatterns = [
    path('', index, name='index')
]


# Create your views here.
