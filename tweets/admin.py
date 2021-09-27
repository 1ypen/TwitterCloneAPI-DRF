from django.contrib import admin

from .models import Tweets, TweetImage

admin.site.register(Tweets)
admin.site.register(TweetImage)