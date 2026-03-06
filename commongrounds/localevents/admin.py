from django.contrib import admin
from .models import EventType, Event


class EventInLine(admin.TabularInline):
    model = Event
    extra = 1
    fields = ("title", "location", "start_time", "end_time")


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inLines = [EventInLine]


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


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
