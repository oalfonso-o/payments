from djmoney.money import Money
from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth.models import User

from payments.models import Payment


class ApiPaymentTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.sender_user = User(id=101, username='admin', password='admin')
        self.sender_user.save()
        self.client.force_authenticate(user=self.sender_user)
        self.receiver_user = User(id=102, username='oriol', password='oriol')
        self.receiver_user.save()
        self.friend_of_receiver = User(username='guido', password='guido')
        self.friend_of_receiver.save()

    def test_payment_get(self):
        empty_response = self.client.get('/api/payments/')
        self.assertEqual(empty_response.status_code, 200)
        self.assertEqual(empty_response.data, [])

        payment1 = Payment(
            sender=self.sender_user, receiver=self.receiver_user, amount=10
        )
        payment1.save()
        payment2 = Payment(
            sender=self.receiver_user, receiver=self.sender_user, amount=50
        )
        payment2.save()
        payment3 = Payment(
            sender=self.receiver_user,
            receiver=self.friend_of_receiver,
            amount=50,
        )
        payment3.save()

        response = self.client.get('/api/payments/')
        self.assertEqual(len(response.data), 2)

        first_payment = response.data[0]
        self.assertEqual(first_payment['sender']['username'], 'admin')
        self.assertEqual(first_payment['receiver']['username'], 'oriol')
        self.assertEqual(first_payment['amount'], '10.00')

        second_payment = response.data[1]
        self.assertEqual(second_payment['sender']['username'], 'oriol')
        self.assertEqual(second_payment['receiver']['username'], 'admin')
        self.assertEqual(second_payment['amount'], '50.00')

    def test_payment_post(self):
        receiver_not_found_response = self.client.post(
            '/api/payments/',
            '{"amount": 1, "receiver": 123}',
            content_type='application/json',
        )
        self.assertEqual(
            receiver_not_found_response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            receiver_not_found_response.data,
            {'error': 'Receiver user not found'},
        )

        same_receiver_and_sender_response = self.client.post(
            '/api/payments/',
            '{"amount": 1, "receiver": 101}',
            content_type='application/json',
        )
        self.assertEqual(
            same_receiver_and_sender_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            same_receiver_and_sender_response.data,
            {'error': 'Receiver user is the same as sender'},
        )

        not_enough_money_response = self.client.post(
            '/api/payments/',
            '{"amount": 100.01, "receiver": 102}',
            content_type='application/json',
        )
        self.assertEqual(
            not_enough_money_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            not_enough_money_response.data,
            {'error': 'You don\'t have enough money'},
        )

        created_response = self.client.post(
            '/api/payments/',
            '{"amount": 100, "receiver": 102}',
            content_type='application/json',
        )
        self.assertEqual(created_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_response.data['sender'], 101)
        self.assertEqual(created_response.data['receiver'], 102)
        self.assertEqual(created_response.data['amount'], '100.00')

        self.sender_user.refresh_from_db()
        self.receiver_user.refresh_from_db()
        self.assertEqual(self.sender_user.account.balance, Money(0, 'EUR'))
        self.assertEqual(self.receiver_user.account.balance, Money(200, 'EUR'))
