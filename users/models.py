import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError("Email must be given!")
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)

        user = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **kwargs):
        if not email:
            raise ValueError("Email must be given!")
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_verified", True)
        kwargs.setdefault("is_staff", True)

        superuser = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    email = models.EmailField(max_length=250, unique=True, db_index=True)
    username = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=200, null=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True, null=False)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["id", "email", "username"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_perms(self, perm, obj=None):
        return self.is_superuser

    def get_full_name(self) -> str:
        return self.username

    def has_module_perms(self, app_label):
        return True
