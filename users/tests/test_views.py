from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import Account
from users.signals import user_created


class CreateAPIViewTest(APITestCase):
    def setUp(self):
        self.data = {
            "email": "janedoe@gmail.com",
            "password": "Password@123",
            "username": "janey",
        }

        return self.data

    def test_create_user_view(self):
        url = reverse("users:register")

        response = self.client.post(url, self.data, format="json")
        response_data = response.json()
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.key}')

        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["message"], "User Created Successfully!")

        # self.assertIn("token", response_data)
        # token = response_data["token"]
        # self.assertEqual(response_data["token"], f"{token}")

        self.assertTrue(user_created.has_listeners(settings.AUTH_USER_MODEL))
        self.assertEqual(Account.objects.count(), 1)

        # print(response.content)


class LoginAPISTestcase(APITestCase):
    def setUp(self):
        self.data = {
            "email": "janedoe@gmail.com",
            "password": "Password@123",
            "username": "janey",
        }

        self.user = Account.objects.create_user(**self.data)
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.acesstoken = self.client.post(
            reverse("users:register"), self.data, format="json"
        )

    def test_login_user(self):
        url = reverse("users:login")

        login_data = {
            "username_or_email": "janedoe@gmail.com",
            "password": "Password@123",
        }

        access_token_response = self.client.post(url, login_data)
        access_token_data = access_token_response.json()
        print(access_token_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token_data}")

        self.assertEqual(
            access_token_data.get("message"),
            # f"{self.user.username} logged in successfully!",
            "User Logged in Successfully!",
        )
        self.assertTrue(status.HTTP_200_OK)
        self.assertIn("token", access_token_data)
        self.assertEqual(access_token_data["token"], f"{self.token.key}")
        print(access_token_data)


class AuthenticateRequiredAPIViewsTestcase(APITestCase):
    def setUp(self):
        """signup requirement"""
        self.data = {
            "email": "janedoe@gmail.com",
            "password": "Password@123",
            "username": "janey",
        }

        self.user = Account.objects.create_user(**self.data)
        token = Token.objects.get_or_create(user=self.user)

        """
         login requirement
        """
        self.login_data = {
            "username_or_email": "janedoe@gmail.com",
            "password": "Password@123",
        }

        self.access_token = self.client.post(
            reverse("users:login"), self.login_data, format="json"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_retrieving_a_single_user(self):
        user = self.user
        self.account = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
        }
        url = reverse("users:account_settings")

        response = self.client.get(url)
        response_data = response.json()
        # print(response_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["email"], self.data["email"])
        self.assertEqual(response_data["username"], self.data["username"])

        # self.assertTrue(response.data)

        # self.assertEqual(response_data, self.account)
        # self.assertEqual(response_data["id"], f"{self.user.id}")
        # self.assertEqual(response_data["email"], self.account["email"])
        # self.assertEqual(response_data["username"], self.account["username"])

    def test_update_user_detail(self):
        url = reverse("users:account_settings")

        self.update_dets = {"new_username": "jane"}

        response = self.client.put(url, self.update_dets, format="json")
        response_data = response.json()

        self.assertTrue(status.HTTP_200_OK)
        # self.assertEqual(response_data["message"], "Details successfully updated!")
        # print(response_data)

    def test_reset_password(self):
        user = self.user
        url = reverse("users:reset_password")

        self.new_passw = {
            "old_password": "Password@123",
            "new_password": "Password@24",
            "confirm_password": "Password@24",
        }
        response = self.client.put(url, self.new_passw, format="json")
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Password Reset Successful!")
        print(response_data)

    def test_user_logout(self):
        url = reverse("users:logout")

        response = self.client.post(url, format="json")
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Successfully logged out!")
        print(response_data)

    def test_delete_user(self):
        url = reverse("users:account_settings")

        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
