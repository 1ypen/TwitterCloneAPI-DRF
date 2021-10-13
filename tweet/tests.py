from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from .models import Tweet


class TweetTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            email='example@example.com',
            login='some-login',
            name='some-name',
            date_of_birth='2999-03-25',
            password='password123',
        )
        self.test_user.save()

        # The authorisation header is set, which will then be included in all subsequent requests
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_tweet(self):
        url = reverse('tweet-list')

        data = {
            'text': 'some text',
            'images': []
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 1)
