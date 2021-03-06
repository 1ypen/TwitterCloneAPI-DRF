from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey('tweet.Tweet', on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)