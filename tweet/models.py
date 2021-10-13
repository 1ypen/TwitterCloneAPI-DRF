from django.db import models
from django.conf import settings


class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweet')
    text = models.CharField(max_length=280)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tweets_liked', blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.text[:50]


class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to='images/tweet')
