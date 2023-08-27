from typing import Any, Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from django.http.request import HttpRequest


class EmailorUsernameModelBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str | None = ..., password: str | None = ..., **kwargs: Any) -> AbstractBaseUser | None:
        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        
        users = user_model._default_manager.filter(
            Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username)
        )

        for user in users:
            if user.check_password(password):
                return user 
        if not users:
            user_model().set_password(password)
                
        return super().authenticate(request, username, password, **kwargs)








# class EmailOrUsernameModelBackend(ModelBackend): 
#     def authenticate(self, request, username=None, password=None, **kwargs):  
#         user_model = get_user_model()

#         if username is None:
#             username = kwargs.get(user_model.USERNAME_FIELD)

#         users = user_model._default_manager.filter(
#             Q(**{user_model.USERNAME_FIELD: username}) | Q(email__iexact=username)
#         )
#         for user in users:
#             if user.check_password(password):
#                 return user
#         if not users:
#             user_model().set_password(password)