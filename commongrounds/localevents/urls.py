from django.urls import path
from .views import EventCreateView, EventDetailView, EventListView, EventSignupView, EventUpdateView

urlpatterns = [
    path("events/", EventListView.as_view(), name = "event_list"),
    path("event/<int:pk>/", EventDetailView.as_view(), name = "event_detail"), 
    path("event/add/", EventCreateView.as_view(), name = "event_create"), 
    path("event/<int:pk>/edit/", EventUpdateView.as_view(), name = "event_update"),
    path("event/<int:pk>/signup/", EventSignupView.as_view(), name = "event_signup")
]
