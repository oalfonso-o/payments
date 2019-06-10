from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth.models import User


class ApiPaymentTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        admin = User(id=101, username='admin', password='admin')
        admin.save()
        self.client.force_authenticate(user=admin)
        user2 = User(id=102, username='oriol', password='oriol')
        user2.save()
        user3 = User(username='guido', password='guido')
        user3.save()

    def test_user_get(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(
            {'id': 101, 'username': 'admin'}, response.data,
        )
        self.assertIn(
            {'id': 102, 'username': 'oriol'}, response.data,
        )
        self.assertEqual(len(response.data), 2)
