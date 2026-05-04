from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from accounts.mixins import RoleRequiredMixin
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

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user
        if not user.is_authenticated:
            return redirect("event_signup", pk=event.pk)
        profile = user.profile

        if event.organizers.filter(id=profile.id).exists():
            return redirect("event_detail", pk=event.pk)
        if EventSignup.objects.filter(event=event, user_registrant=profile).exists():
            return redirect("event_detail", pk=event.pk)
        if event.signups.count() >= event.event_capacity:
            return redirect("event_detail", pk=event.pk)
        
        EventSignup.objects.create(event=event, user_registrant=profile)
        if event.signups.count() >= event.event_capacity:
            event.status = Event.STATUS_FULL
            event.save()
        return redirect("event_detail", pk=event.pk)


class EventCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ["Event Organizer"]
    model = Event 
    fields = ["title", "category", "event_image", "description", "location", "start_time", "end_time", "event_capacity"]
    template_name = "localevents/event_create.html"
    success_url = reverse_lazy("event_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizers.add(self.request.user.profile)
        return response 
    

class EventUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ["Event Organizer"]
    model = Event
    fields = ["title", "category", "event_image", "description", "location", "start_time", "end_time", "event_capacity"]
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
    def get(self, request, pk):
        if request.user.is_authenticated:
            return redirect("event_detail", pk=pk)
        
        event = get_object_or_404(Event, pk=pk)
        return render(request, "localevents/event_signup.html", {"event":event})
    
    def post(self, request, pk):
        if request.user.is_authenticated:
            return redirect("event_detail", pk=pk)
        event = get_object_or_404(Event, pk=pk)
        name = request.POST.get("name")

        if not name: 
            return render(request, "localevents/event_signup.html", {"event": event, "error": "Name is required."})
        if event.signups.count() >= event.event_capacity:
            return render(request, "localevents/event_signup.html", {"event": event, "error": "Event is already full."})
        if EventSignup.objects.filter(event=event, new_registrant=name).exists():
            return render(request, "localevents/event_signup.html", {"event": event, "error": "You have already signed up."})
        
        EventSignup.objects.create(event=event, new_registrant = name)
        if event.signups.count() >= event.event_capacity:
            event.status = Event.STATUS_FULL
            event.save()

        return redirect("event_detail", pk=event.pk)