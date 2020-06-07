from django.contrib import admin
from .models import Event, Game, User, Platform

# Register your models here.

admin.site.register(Event)
admin.site.register(Game)
admin.site.register(User)
admin.site.register(Platform)
