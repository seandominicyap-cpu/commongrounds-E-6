from django.db import models
from django.urls import reverse


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_AVAILABLE = "Available"
    STATUS_FULL = "Full"
    STATUS_DONE = "Done"
    STATUS_CANCELLED = "Cancelled"
    STATUS_CHOICES = [(STATUS_AVAILABLE, "Available"), (STATUS_FULL, "Full"), (STATUS_DONE, "Done"), (STATUS_CANCELLED, "Cancelled")]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    organizers = models.ManyToManyField("Profile", blank=True)
    event_image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.id)])


class EventSignup(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="signups")
    user_registrant = models.ForeignKey("Profile", on_delete=models.CASCADE, null=True, blank=True, related_name="user_signups")
    new_registrant = models.CharField(max_length=255, null=True, blank=True)