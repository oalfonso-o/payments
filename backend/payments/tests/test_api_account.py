from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth.models import User


class ApiPaymentsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        admin = User(username='admin', password='admin')
        admin.save()
        self.client.force_authenticate(user=admin)

    def test_account_get(self):
        response = self.client.get('/api/account/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '100.00')
