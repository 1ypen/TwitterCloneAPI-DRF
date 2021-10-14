from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Tweet

User = get_user_model()


class TweetTest(APITestCase):
    def setUp(self):
        self.test_user_one = User.objects.create(
            email='example1@example.com',
            login='some-login1',
            name='some-name1',
            date_of_birth='2999-03-25',
            password='password123',
        )
        self.test_user_one.save()

        self.test_user_two = User.objects.create(
            email='example2@example.com',
            login='some-login2',
            name='some-name2',
            date_of_birth='2999-03-25',
            password='password123',
        )
        self.test_user_two.save()

        for i in range(5):
            Tweet.objects.create(text=f'test {i}', user=self.test_user_one).save()
        for i in range(5):
            Tweet.objects.create(text=f'test {i}', user=self.test_user_two).save()

        # The authorisation header is set, which will then be included in all subsequent requests
        refresh = RefreshToken.for_user(self.test_user_one)
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
        self.assertEqual(response.data['user_login'], self.test_user_one.login)
        self.assertEqual(response.data['user_name'], self.test_user_one.name)
        self.assertEqual(Tweet.objects.count(), count_of_tweet + 1)

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

    def test_tweet_delete(self):
        url = reverse('tweet-delete-ajax')

        count_of_tweet = Tweet.objects.filter(is_active=True).count()

        # Correct data
        response = self.client.delete(url, data={'id': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tweet.objects.filter(is_active=True).count(), count_of_tweet - 1)

        response = self.client.delete(url, data={'id': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Wrong data
        # checking that a tweet can only be deleted by the creator
        refresh = RefreshToken.for_user(self.test_user_two)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = self.client.delete(url, data={'id': 2}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Tweet.objects.filter(is_active=True).count(), count_of_tweet - 1)

    def test_tweet_like(self):

        url = reverse('tweet-like-ajax')

        number_of_likes_for_a_tweet = Tweet.objects.get(id=1).users_like.count()

        response = self.client.post(url, {'id': 1, 'action': 'like'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.get(id=1).users_like.count(), number_of_likes_for_a_tweet + 1)
        # checking that one user cannot put multiple likes on one tweet
        response = self.client.post(url, {'id': 1, 'action': 'like'}, format='json')
        self.assertEqual(Tweet.objects.get(id=1).users_like.count(), number_of_likes_for_a_tweet + 1)

        # check for dislike
        response = self.client.post(url, {'id': 1, 'action': 'dislike'}, format='json')
        self.assertEqual(Tweet.objects.get(id=1).users_like.count(), number_of_likes_for_a_tweet)

        # check for a non-existent tweet
        response = self.client.post(url, {'id': 100, 'action': 'dislike'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
