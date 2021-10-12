from django.db.models import Count, Case, When, F
from rest_framework import serializers

from .models import Tweet, TweetImage


class CustomListImageSerializer(serializers.ListField):
    def to_representation(self, data):
        if type(data) == str:
            return [data]
        return [self.child.to_representation(item) if item is not None else None for item in data]


class TweetSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    user_login = serializers.CharField(read_only=True)
    user_avatar = serializers.URLField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True, default=0)
    reply_count = serializers.IntegerField(read_only=True, default=0)
    comment_count = serializers.IntegerField(read_only=True, default=0)
    img = CustomListImageSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user_name', 'user_login', 'user_avatar', 'created_date', 'text', 'img', 'is_liked',
                  'like_count', 'reply_count', 'comment_count']


class TweetCreateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255)
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data.pop('text')
        images = validated_data.pop('images')

        tweet = Tweet.objects.create(user=user, text=text)

        images_object = [TweetImage.objects.create(tweet=tweet, img=image) for image in images]

        return tweet, images_object

    def to_representation(self, instance):
        tweet, images = instance
        user = self.context['request'].user
        object = {**tweet.__dict__,
                  'user_name': user.name,
                  'user_login': user.login,
                  'user_avatar': user.avatar,
                  'img': images
                  }
        return TweetSerializer(object).data
