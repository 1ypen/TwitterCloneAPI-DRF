from django.contrib import admin

from .models import Tweet, TweetImage

admin.site.register(Tweet)
admin.site.register(TweetImage)