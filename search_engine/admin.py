from django.contrib import admin
from .models import Song, Anime, Artist

admin.site.register([Song, Anime, Artist])
