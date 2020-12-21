from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer


class UserRegistrationTestCase(APITestCase):

	def test_registration(self):
		data = {'email': 'test@yandex.ru', 'password': 'DNHnxvxF', 'wms_id': '3420'}
		response = self.client.post('/auth/users/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ShiftTestCase(APITestCase):

	def test_registration(self):
		data = {'email': 'test@yandex.ru', 'password': 'DNHnxvxF', 'wms_id': '3420'}
		response = self.client.post('/auth/users/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

