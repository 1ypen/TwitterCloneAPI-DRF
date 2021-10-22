from django.contrib import admin

from .models import Tweet, TweetImage, Bookmark

admin.site.register(Tweet)
admin.site.register(TweetImage)
admin.site.register(Bookmark)
