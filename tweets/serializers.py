from rest_framework import serializers

from .models import Tweets, TweetImage


class CustomListImageSerializer(serializers.ListField):
    def to_representation(self, data):
        if type(data) == str:
            return [data]
        return [self.child.to_representation(item) if item is not None else None for item in data]


class TweetsListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    user_login = serializers.CharField(read_only=True)
    user_avatar = serializers.URLField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True, default=0)
    comment_count = serializers.IntegerField(read_only=True, default=0)
    img = CustomListImageSerializer(read_only=True)

    class Meta:
        model = Tweets
        fields = ['id', 'user_name', 'user_login', 'user_avatar', 'created_date', 'text', 'img', 'is_liked',
                  'like_count', 'reply_count', 'comment_count']


class TweetCreateSerializer(serializers.Serializer):

    text = serializers.CharField(max_length=255)
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    def create(self, validated_data):

        print(self.context['request'].data)

        user = self.context['request'].user
        text = validated_data.pop('text')
        images = validated_data.pop('images')

        tweet = Tweets.objects.create(user=user, text=text)

        for image in images:
            TweetImage.objects.create(tweet=tweet, img=image)

        return tweet

    def to_representation(self, instance):
        return TweetsListSerializer(instance).data