from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
# Create your tests here.

class RegisterUserTests(APITestCase):
    def setUp(self):
        self.data = data = {'username': '098jonathan', 'first_name': 'john', 'last_name': 'doe', 'email': 'john@gmail.com'}
        data['password'] = '098johndoe'
        self.client = APIClient()

    def test_should_return_400_if_invalid_data_is_sent(self):
        response = self.client.post('/accounts/signin', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_201_status_code_if_valid_is_sent(self):
        response = self.client.post('/accounts/signin', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
    
    def test_should_return_data_if_request_successfull(self):
        response = self.client.post('/accounts/signin', self.data, format='json') 
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['token'], str)
        self.assertGreater(len(response.data['token']), 0)
        self.assertIsInstance(response.data['id'], int)

    def test_should_not_return_hashed_password_in_response(self):
        response = self.client.post('/accounts/signin', self.data, format='json') 
        self.assertNotIn('password', response.data.keys())



class LoginUserTest(APITestCase):
    def setUp(self):
        self.initial_data = {'username': 'john', 'first_name': 'john', 'last_name': 'doe', 'email': 'john@gmail.com'}
        self.password = '098johndoe'
        self.client = APIClient()
        initial_user = User(**self.initial_data)
        initial_user.set_password(self.password)
        initial_user.save()

        Token.objects.create(user=initial_user)

        self.client = APIClient()

    def test_should_return_400_status_code_if_invalid_data_is_sent(self):
        response = self.client.post('/accounts/login', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_404_status_code_if_cannot_find_user(self):
        data = {'username': 'daydate', 'password': '098daydate'}
        response = self.client.post('/accounts/login', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_200_status_code_if_valid_data_is_sent(self):
        response = self.client.post('/accounts/login', 
          {'username': self.initial_data['username'], 'password': self.password},
          format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_object_if_request_successfull(self):
        response = self.client.post('/accounts/login', 
        {'username': self.initial_data['username'], 'password': self.password},
          format='json'
        )
        self.assertIsInstance(response.data, dict)
        self.assertIsInstance(response.data['token'], str)
        self.assertGreater(len(response.data['token']), 0)
        self.assertIsInstance(response.data['id'], int)
