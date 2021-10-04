from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    user_name = serializers.CharField(read_only=True)
    user_login = serializers.CharField(read_only=True)
    user_avatar = serializers.URLField(read_only=True)

    class Meta:
        model = Comment
        exclude = ('user', 'tweet')