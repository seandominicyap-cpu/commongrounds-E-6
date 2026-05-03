from django.contrib import admin
from .models import EventType, Event, EventSignup
from accounts.models import Profile, Role


class EventInLine(admin.TabularInline):
    model = Event
    extra = 1
    fields = ("title", "location", "start_time", "end_time")


class EventSignupInLine(admin.TabularInline):
    model = EventSignup
    extra = 0

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [EventInLine]


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "start_time",
        "end_time",
        "location",
        "created_on",
        "updated_on",
    )
    list_filter = ("category", "start_time")
    search_fields = ("title", "description", "location")
    inlines = [EventSignupInLine]


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSignup)

admin.site.register(Profile)
admin.site.register(Role)