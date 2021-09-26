from datetime import datetime, timezone

from rest_framework import serializers

from .models import Tweets


class TweetsListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField()
    user_avatar = serializers.URLField()
    is_liked = serializers.BooleanField()
    like_count = serializers.IntegerField()
    created_date = serializers.SerializerMethodField(method_name='get_formatted_creation_date')

    class Meta:
        model = Tweets
        fields = ['id', 'user_name', 'user_avatar', 'created_date', 'text', 'is_liked', 'like_count']

    def get_formatted_creation_date(self, obj: dict) -> str:
        """
        returns the formatted date of creation of the tweet in the form
        1m if the tweet was created a minute ago
        1h if the tweet was created an hour ago etc
        """
        created_date = obj.get('created_date')
        time_now = datetime.now(timezone.utc)
        time_period = abs(created_date - time_now)

        hours, remainder = divmod(time_period.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if time_period.days >= 365:
            return created_date.strftime('%b %-d, %Y')

        if time_period.days >= 1:
            return created_date.strftime('%b %-d')

        if 1 <= hours <= 24:
            return created_date.strftime('%-Hh')

        if minutes:
            return f'{minutes}m'

        if seconds:
            return f'{seconds}s'

        return '0s'
