from django.db import models

from datetime import datetime, timezone

from accounts.models import User


VISIBILITY_CHOICES = (('followers', 'only followers'),
                      ('follow', 'only my subscriptions'),
                      ('all', 'all'))


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet')
    text = models.CharField(max_length=280)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(User, related_name='tweets_liked', blank=True)
    visibility = models.CharField(max_length=55, choices=VISIBILITY_CHOICES, default='all')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.text[:50]


class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='images/tweet')