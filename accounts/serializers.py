from rest_framework import serializers

from .models import User


class UserSerializerForTweet(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'login', 'avatar']
