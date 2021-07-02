from datetime import timedelta

from api.factories import TransactionFactory, UserFactory
from api.models import Transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status


class UserTestCase(TestCase):

    def setUp(self):
        self.url = reverse('user-list')

    def test_user_create(self):
        payload = {"name": "Jane Doe", "email": "jane@email.com", "age": 23}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payload['name'], response.data['name'])


class TransactionTestCase(TestCase):

    def post_request(self, url, payload):
        return self.client.post(url, payload, content_type='application/json')

    def setUp(self):
        self.url = reverse('transaction-list')
        self.user = UserFactory(
            name="Jane Doe", email="jane@email.com", age=23)
        self.payload = {
            "reference": "000051",
            "account": "S00099",
            "date": "2020-01-13",
            "amount": "-51.13",
            "type": "outflow",
            "category": "groceries",
            "user_id": self.user.pk
        }

    def test_create(self):
        response = self.post_request(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload['reference'], response.data['reference'])

    def test_type_validation(self):
        self.payload['type'] = 'inflow'
        response = self.post_request(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['type'][0],
            'Wrong transaction type with reference: 000051'
        )

    def test_duplicate(self):
        response = self.post_request(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.post_request(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['reference'][0],
            'transaction with this reference already exists.'
        )

    def test_create_bulk(self):
        payload = [{
            "reference": "000051"+str(i),
            "account": "S00099",
            "date": "2020-01-13",
            "amount": "-51.13",
            "type": "outflow",
            "category": "groceries",
            "user_id": self.user.pk
        } for i in range(0, 2)]
        response = self.post_request(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, list))

    def test_create_bulk_with_duplicates(self):
        payload = [{
            "reference": "000051",
            "account": "S00099",
            "date": "2020-01-13",
            "amount": "-51.13",
            "type": "outflow",
            "category": "groceries",
            "user_id": self.user.pk
        } for i in range(0, 2)]
        response = self.post_request(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(Transaction.objects.all().count() == 1)


class AccountSummaryTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(
            name="Jane Doe", email="jane@email.com", age=23)
        self.accounts = {"A": "S00099", "B": "S00091"}
        self.amounts = {"A": "-51.13", "B": "51.13"}
        for i in range(0, 3):
            TransactionFactory(
                reference="000051"+str(i),
                account=self.accounts['A'],
                date=now().date() - timedelta(days=i),
                amount=self.amounts['A'],
                type="outflow",
                category="groceries",
                user_id=self.user
            )
        for i in range(0, 3):
            TransactionFactory(
                reference="0013123411"+str(i),
                account=self.accounts['B'],
                date=now().date() - timedelta(days=i),
                amount=self.amounts['B'],
                type="inflow",
                category="salary",
                user_id=self.user
            )
        self.url = reverse('user-account-summary', args=[self.user.pk])

    def test_total(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.accounts))
        self.assertEqual(
            response.data[0]['balance'], response.data[0]['total_inflow'])
        self.assertEqual(
            response.data[1]['balance'], response.data[1]['total_outflow'])

    def test_by_date_range(self):
        date_from = now().date()
        date_to = date_from + timedelta(days=1)
        response = self.client.get(
            self.url+f'?date_from={date_from}&date_to={date_to}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['balance'], self.amounts['B'])
        self.assertEqual(response.data[1]['balance'], self.amounts['A'])


class CategorySummaryTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(
            name="Jane Doe", email="jane@email.com", age=23)
        self.categories = {"A": "groceries", "B": "salary"}
        self.amounts = {"A": "-51.13", "B": "51.13"}
        for i in range(0, 3):
            TransactionFactory(
                reference="000051"+str(i),
                account='S00341353'+str(i),
                date=now().date() - timedelta(days=i),
                amount=self.amounts['A'],
                type="outflow",
                category=self.categories['A'],
                user_id=self.user
            )
        for i in range(0, 3):
            TransactionFactory(
                reference="0013123411"+str(i),
                account='S00099'+str(i),
                date=now().date() - timedelta(days=i),
                amount=self.amounts['B'],
                type="inflow",
                category=self.categories['B'],
                user_id=self.user
            )
        self.url = reverse('user-category-summary', args=[self.user.pk])

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['inflow'][self.categories['B']])
        self.assertTrue(response.data['outflow'][self.categories['A']])
        self.assertEqual(
            response.data['inflow'][self.categories['B']],
            str(round(float(self.amounts['B'])*3, 2))
        )
