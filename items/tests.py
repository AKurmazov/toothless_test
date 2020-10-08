import json

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse
from django.db.utils import DataError

from items.models import Item


class CreateItemTest(TestCase):

    def test_create_item_success_usd(self):
        data = {
            'name': 'test',
            'description': 'test',
            'price': 0.5,
            'currency': 'USD',
        }
        item = Item.objects.create(**data)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.description, data['description'])
        self.assertEqual(item.price, data['price'])
        self.assertEqual(item.currency, data['currency'])

    def test_create_item_success_rub(self):
        data = {
            'name': 'test',
            'description': 'test',
            'price': 40.0,
            'currency': 'RUB',
        }
        item = Item.objects.create(**data)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.description, data['description'])
        self.assertEqual(item.price, data['price'])
        self.assertEqual(item.currency, data['currency'])

    def test_create_item_success_no_description(self):
        data = {
            'name': 'test',
            'price': 40.0,
            'currency': 'RUB',
        }
        item = Item.objects.create(**data)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.description, '')
        self.assertEqual(item.price, data['price'])
        self.assertEqual(item.currency, data['currency'])

    def test_create_item_success_no_description_and_currency(self):
        data = {
            'name': 'test',
            'price': 40.0,
        }
        item = Item.objects.create(**data)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.description, '')
        self.assertEqual(item.price, data['price'])
        self.assertEqual(item.currency, 'USD')

    def test_create_item_failure_wrong_currency(self):
        data = {
            'name': 'test',
            'price': 40.0,
            'currency': 'EUR'
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)

    def test_create_item_failure_missing_price(self):
        data = {
            'name': 'test',
            'currency': 'USD'
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)

    def test_create_item_failure_violates_name_max_length_constraint(self):
        data = {
            'name': 'c' * 129,
            'price': 40.0,
        }
        self.assertRaises(DataError, Item.objects.create, **data)

    def test_create_item_failure_violates_minimum_price_constraint_usd(self):
        data = {
            'name': 'test',
            'price': 0.49,
            'currency': 'USD',
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)

    def test_create_item_failure_violates_maximum_price_constraint_usd(self):
        data = {
            'name': 'test',
            'price': 99999999.9,
            'currency': 'USD',
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)

    def test_create_item_failure_violates_minimum_price_constraint_rub(self):
        data = {
            'name': 'test',
            'price': 39.9,
            'currency': 'RUB',
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)

    def test_create_item_failure_violates_maximum_price_constraint_rub(self):
        data = {
            'name': 'test',
            'price': 99999999.9,
            'currency': 'RUB',
        }
        self.assertRaises(ValidationError, Item.objects.create, **data)


class IndexViewTest(TestCase):

    def test_index_view_success(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class ThanksViewTest(TestCase):

    def test_index_view_success(self):
        response = self.client.get(reverse('thanks'))
        self.assertEqual(response.status_code, 200)


class ItemDetailsViewTest(TestCase):

    item_data = {
        'name': 'test',
        'description': 'test',
        'price': 0.5,
        'currency': 'USD'
    }

    def setUp(self):
        self.item = Item.objects.create(**self.item_data)

    def test_item_details_view_success(self):
        response = self.client.get(reverse('item_details', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_item_details_view_failure_item_does_not_exist(self):
        kwargs = {
            'pk': 1000
        }
        response = self.client.get(reverse('item_details', kwargs=kwargs))
        self.assertEqual(response.status_code, 404)


class BuyItemViewTest(TestCase):

    item_data = {
        'name': 'test',
        'description': 'test',
        'price': 0.5,
        'currency': 'USD'
    }

    def setUp(self):
        self.item = Item.objects.create(**self.item_data)

    def test_buy_item_view_success(self):
        response = self.client.get(reverse('buy_item', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)

        json_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('session_id', json_data.keys())
        self.assertIsNotNone(json_data['session_id'])

    def test_buy_item_view_failure_item_does_not_exist(self):
        kwargs = {
            'pk': 1000
        }
        self.assertRaises(ObjectDoesNotExist, Item.objects.get, **kwargs)

        response = self.client.get(reverse('buy_item', kwargs=kwargs))
        self.assertEqual(response.status_code, 404)

        json_data = json.loads(response.content.decode('utf-8'))
        self.assertIn('Message', json_data.keys())
        self.assertEqual(json_data['Message'], 'Not found.')
