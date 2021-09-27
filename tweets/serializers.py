from datetime import datetime, timezone

from rest_framework import serializers

from .models import Tweets


class TweetsListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    user_avatar = serializers.URLField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tweets
        fields = ['id', 'user_name', 'user_avatar', 'created_date', 'text', 'is_liked', 'like_count']

    def create(self, validated_data):
        user = self.context['request'].user
        tweets = Tweets.objects.create(user=user, **validated_data)
        return tweets