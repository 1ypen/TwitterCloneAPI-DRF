from django.db import models


class Comment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    tweet = models.ForeignKey('tweet.Tweet', on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)