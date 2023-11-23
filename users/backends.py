from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.http.request import HttpRequest


class EmailorUsernameModelBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: str | None,
        password: str | None,
        **kwargs: Any
    ) -> AbstractUser | None:
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None


