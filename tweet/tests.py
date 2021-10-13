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

        for i in range(10):
            Tweet.objects.create(text=f'test {i}', user=self.test_user).save()

        # The authorisation header is set, which will then be included in all subsequent requests
        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_tweet(self):
        url = reverse('tweet-list')

        # Correct data
        data = {
            'text': 'some text',
            'images': []
        }

        count_of_tweet = Tweet.objects.count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], data['text'])
        self.assertEqual(response.data['img'], data['images'])
        self.assertEqual(response.data['user_avatar'], '')
        self.assertEqual(response.data['user_login'], self.test_user.login)
        self.assertEqual(response.data['user_name'], self.test_user.name)
        self.assertEqual(Tweet.objects.count(), count_of_tweet+1)

        # Wrong data
        data = {
            'text': '',
            'images': []
        }

        count_of_tweet = Tweet.objects.count()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tweet.objects.count(), count_of_tweet)

    def test_tweet_detail(self):

        # Correct data
        url = reverse('tweet-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

        # Wrong data
        url = reverse('tweet-detail', kwargs={'pk': 11})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tweet_list(self):
        url = reverse('tweet-list')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Tweet.objects.count())
