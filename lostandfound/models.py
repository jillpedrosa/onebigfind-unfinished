from django.db import models
from django.contrib.auth.models import User

class LostItem(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=30, blank=True)
    unique_features = models.TextField(blank=True)
    date_lost = models.DateField()
    location_lost = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)  # Image field
    is_matched = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_lost']

class FoundItem(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=30, blank=True)
    unique_features = models.TextField(blank=True)
    date_found = models.DateField()
    location_found = models.CharField(max_length=100)
    image = models.ImageField(upload_to='found_items/', blank=True, null=True)  # Image field
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='found_items', null=True)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_found']