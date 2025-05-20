from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "House A"
    description = models.TextField(blank=True)  # e.g., "Family home bought in 1995"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AbuseType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Financial"
    color = models.CharField(max_length=7, blank=True)  # e.g., "#4CAF50"

    def __str__(self):
        return self.name

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=200)  # e.g., "Purchased in Our Names"
    date = models.DateField()  # e.g., 1995-03-15
    description = models.TextField()  # Summary for card
    details = models.TextField(blank=True)  # For overlay
    abuse_types = models.ManyToManyField(AbuseType)  # e.g., Financial, Legal
    icon = models.CharField(max_length=50, blank=True)  # e.g., "house"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date.year}: {self.name} ({self.group})"

    class Meta:
        ordering = ["date"]

class EventFile(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.event}"

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()  # e.g., "This event caused financial strain"
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.event} by {self.user}"

    class Meta:
        ordering = ["date"]