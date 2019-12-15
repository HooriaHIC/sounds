from django.contrib import admin
from .models import Music, Playlist, Album, Like

# Register your models here.
admin.site.register(Music)
admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(Like)
