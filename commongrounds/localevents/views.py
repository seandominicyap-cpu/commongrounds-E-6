from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventSignup


class EventListView(ListView):
    model = Event
    template_name = "localevents/events_list.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        created = Event.objects.none()
        signed_up = Event.objects.none()
        other = Event.objects.all()

        if user.is_authenticated:
            user_profile = user.profile
            created = Event.objects.filter(organizers=user_profile)
            signed_up = Event.objects.filter(signups__user_registrant=user_profile).distinct()
            other = Event.objects.exclude(id__in=created.values("id")).exclude(id__in=signed_up.values("id"))

        ctx["created_events"] = created
        ctx["signed_up_events"] = signed_up
        ctx["other_events"] = other
        return ctx


class EventDetailView(DetailView):
    model = Event
    template_name = "localevents/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user
        signups_count = event.signups.count()
        is_full = signups_count >= event.event_capacity
        is_owner = False
        user_signed_up = False

        if user.is_authenticated:
            profile = user.profile 
            is_owner = event.organizers.filter(id=profile.id).exists()
            user_signed_up = event.signups.filter(user_registrant=profile).exists()

        can_signup = (user.is_authenticated and not is_owner and not is_full and not user_signed_up)

        ctx["is_owner"] = is_owner
        ctx["is_full"] = is_full
        ctx["can_signup"] = can_signup
        ctx["user_signed_up"] = user_signed_up
        return ctx


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event 
    fields = ["title", "category", "event_image", "description", "location", "start_time", "end_time", "event_capacity", "status"]
    template_name = "localevents/event_create.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = self.request.user.profile
        self.object.organizers.add(profile)
        return response 
    

class EventsUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    field = ["title", "category", "event_image", "description", "location", "start_time", "end_time", "event_capacity", "status"]
    template_name = "localevents/event_update.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        event = self.object 
        signup_count = event.signups.count()

        if signup_count >= event.event_capacity:
            event.status = Event.STATUS_FULL
        else:
            event.status = Event.STATUS_AVAILABLE
        event.save()
        return response
    

class EventSignupView(View):
    def get(self, request, event_id):
        if request.user.is_authenticated:
            return redirect("event_detail", pk=event_id)
        
        event = get_object_or_404(Event, id=event_id)
        return render(request, "localevents/signup.html", {"event":event})
    
    def post(self, request, event_id):
        if request.user.is_authenticated:
            return redirect("event_detail", pk=event_id)
        event = get_object_or_404|(Event, id=event_id)
        name = request.POST.get("name")

        if not name: 
            return render(request, "localevents/event_signup.html", {"event": event, "error": "Name is required."})
        
        if event.signups.count() >= event.event_capacity:
            return render(request, "localevents/event_signup.html", {"event": event, "error": "Event is already full"})
        
        EventSignup.objects.create(event=event, new_registrant = name)
        return redirect("event_detail", pk=event.id)