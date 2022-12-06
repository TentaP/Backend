from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tentap.models import User

# Create your tests here.
baseURL = "http://localhost:8000/api/"


class AccountTests(APITestCase):
    def test_signup(self):
        url = baseURL + "signup"
        data = {
            "username": "nour",
            "email": "noubah@gmail.com",
            "password": "t"
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(User.objects.get().username, "nour")
        self.assertEqual(User.objects.get().email, "noubah@gmail.com")
