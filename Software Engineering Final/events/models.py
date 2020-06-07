from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Groups: name, members, genre(?)
# TODO: add __str__() methods


class User(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True, blank=False)
    email = models.EmailField(db_index=True, unique=True, blank=False)
    discord = models.CharField(
        max_length=255, default=None, blank=True, null=True
    )
    email_notifications = models.BooleanField(default=True)
    discord_notifications = models.BooleanField(default=False)
    info = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=(self.id,))


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    platform = models.ForeignKey(Platform, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return "{} | {}".format(self.name, self.platform)


class Event(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_creator"
    )
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(auto_now=True)
    attendees = models.ManyToManyField(User, blank=True, related_name="event_attendes")
    description = models.TextField(blank=True)
    games = models.ManyToManyField(Game, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.start_datetime > self.end_datetime:
            raise Exception("Event cannot start after end date")
        super(Event, self).save(*args, **kwargs)