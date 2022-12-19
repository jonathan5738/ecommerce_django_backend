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


class ManageUserTests(APITestCase):
    def setUp(self):
        self.initial_data = {'username': 'john', 'first_name': 'john', 'last_name': 'doe', 'email': 'john@gmail.com'}
        self.password = '098johndoe'
        self.client = APIClient()
        initial_user = User(**self.initial_data)
        initial_user.set_password(self.password)
        initial_user.save()

        self.token = Token.objects.create(user=initial_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_should_return_400_status_code_if_invalid_data_is_sent(self):
        response = self.client.patch('/accounts/manage', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_should_return_200_status_code_if_valid_data_is_sent(self):
        response = self.client.patch('/accounts/manage', {'username': self.initial_data.get('username')}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_should_return_user_token_and_id_if_request_is_sucessfull(self):
        response = self.client.patch('/accounts/manage', {'first_name': str.upper(self.initial_data.get('first_name'))}, format='json')
        self.assertIsInstance(response.data['id'], int)
        self.assertIsInstance(response.data['token'], str)
        self.assertGreater(len(response.data['token']), 0)

    def test_should_modified_user_in_database_if_request_is_successfull(self):
        self.client.patch('/accounts/manage', {'username': str.upper(self.initial_data.get('username'))}, format='json')
        updated_user = User.objects.get(username=str.upper(self.initial_data.get('username')))
        self.assertIsInstance(updated_user, User)
        self.assertEqual(updated_user.username, str.upper(self.initial_data.get('username')))