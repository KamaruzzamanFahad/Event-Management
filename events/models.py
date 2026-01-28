from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    imagelink = models.ImageField(upload_to='event_images/', blank=True, null=True, default='/event_images/default.jpg')
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    participants = models.ManyToManyField(User, through='RSVP', related_name='rsvp_events')
    location = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RSVP(models.Model):
    rsvp_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rsvp_status = models.CharField(max_length=20, choices=[('attending', 'Attending'), ('not_attending', 'Not Attending')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"



