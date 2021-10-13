from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserTest(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            email='example@example.com',
            login='some-login',
            name='some-name',
            date_of_birth='2999-03-25',
            password='password123',
        )
        self.test_user.save()

        refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        url = reverse('user-list')
        data = {
                "name": "Erlan",
                "email": "fdokpy@gmail.com",
                "date_of_birth": '2004-03-25',
                "login": "lypen",
                "password": "password312"
        }

        count_of_user = User.objects.count()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), count_of_user+1)

        # check for validation of unique user fields (email, login)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), count_of_user+1)

