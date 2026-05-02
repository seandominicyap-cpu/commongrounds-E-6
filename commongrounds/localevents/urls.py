from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.event_list, name="event_list"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),
    path("event/add/", views.event_create, name="event_create"), 
    path("event/<int:event_id>/edit/", views.event_update, name="event_update" ),
    path("event/<int:event_id>/signup/", views.event_signup, name="event_signup"),
]
