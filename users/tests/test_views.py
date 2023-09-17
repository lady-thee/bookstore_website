from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from django.conf import settings

from users.models import UserAccount
from users.serializers import UserSerializer, UpdateUserSerializer, LoginSerializer
from users.signals import user_created


class CreateAPIViewTestcase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "email": "janedoe@gmail.com",
            "password": "2030",
            "username": "janey"
        }

        # self.user = UserAccount.objects.create_user(**self.data)
        # self.token = Token.objects.get(user=self.user)
        return self.data
    

    def test_create_endpoint(self):
        url = reverse("create")
        serializer = UserSerializer(data=self.data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        # self.user = UserAccount.objects.create_user(**self.data)
        # self.token = Token.objects.get(user=self.user)
        
        self.assertTrue(serializer.save())
        self.token = Token.objects.get(user=serializer.instance)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token: {self.token.key}')
        response = self.client.post(url, self.data, format='json')
        
        print(self.token, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user_created.has_listeners(settings.AUTH_USER_MODEL))
        self.assertEqual(UserAccount.objects.count(), 1)
        self.assertTrue(response.data['message'], 'User successfully created!')


class LoginAPIViewTestcase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "username_or_email": "janedoe@gmail.com",
            "password": "2030"
        }

    def test_login_endpoint(self):
        url = reverse('login')
        self.client.logout()
        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)
        
# class UpdateAPIViewTestcase(APITestCase):
#     def setUp(self):
#         self.data = {
#             "new_username": "john"
#         }
        
#         return self.data

#     def test_update_endpoint(self):
#         url = reverse('update')
#         self.client.login(username='janedoe@gmail.com', password='2030')
#         serializer = UpdateUserSerializer(data=self.data)

#         self.assertTrue(serializer.is_valid(), serializer.errors)
#         response = self.client.put(url, self.data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Details successfully updated!')


        