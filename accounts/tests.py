from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTest(APITestCase):
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

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        # check for validation of unique user fields (email, login)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
