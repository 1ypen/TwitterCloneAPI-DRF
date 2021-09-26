from rest_framework import serializers

from .models import Tweets
from accounts.serializers import UserSerializerForTweet


# class TweetsListSerializer(serializers.ModelSerializer):
#     user = UserSerializerForTweet()
#     like_count = serializers.IntegerField(source='get_like_count')
#     created_date = serializers.CharField(source='get_formatted_creation_date')
#
#     class Meta:
#         model = Tweets
#         fields = ['id', 'user', 'created_date', 'text', 'like_count']


class TweetsListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField()
    user_avatar = serializers.URLField()
    like_count = serializers.IntegerField()

    class Meta:
        model = Tweets
        fields = ['id', 'user_name', 'user_avatar', 'created_date', 'text', 'like_count']
