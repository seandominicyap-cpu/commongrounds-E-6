from django.db import models
from django.urls import reverse 

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.id)])