from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all()
    ctx = {'events': events}
    return render(request, "localevents/events_list.html", ctx)

def event_detail(request, event_id):
    ctx = {"event": Event.objects.get(id=event_id)}
    return render(request, "localevents/event_detail.html", ctx)
