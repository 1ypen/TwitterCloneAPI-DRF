from django.db import models

from datetime import datetime, timezone

from accounts.models import User


VISIBILITY_CHOICES = (('followers', 'only followers'),
                      ('follow', 'only my subscriptions'),
                      ('all', 'all'))


class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    text = models.CharField(max_length=280)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    users_like = models.ManyToManyField(User, related_name='tweets_liked', blank=True)

    visibility = models.CharField(max_length=55, choices=VISIBILITY_CHOICES, default='all')

    class Meta:
        ordering = ('-created_date',)

    @property
    def get_formatted_creation_date(self):
        """
        returns the formatted date of creation of the tweet in the form
        1m if the tweet was created a minute ago
        1h if the tweet was created an hour ago etc
        """
        time_now = datetime.now(timezone.utc)
        time_period = abs(self.created_date - time_now)

        hours, remainder = divmod(time_period.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if time_period.days >= 365:
            return self.created_date.strftime('%b %-d, %Y')

        if time_period.days >= 1:
            return self.created_date.strftime('%b %-d')

        if 1 <= hours <= 24:
            return self.created_date.strftime('%-Hh')

        if minutes:
            return f'{minutes}m'

        if seconds:
            return f'{seconds}s'

        return '0s'

    def get_like_count(self):
        return self.users_like.all().count()

    def __str__(self):
        return self.text[:50]
