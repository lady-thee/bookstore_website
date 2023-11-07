import uuid
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.urls import reverse


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


class Account(AbstractUser):
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
    date_joined = None
    created_time = models.DateTimeField(auto_now_add=True, null=False)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["id", "email", "username"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.pk})
    
    def get_update_url(self):
        return reverse("users:user_update", kwargs={"pk": self.pk})
    
    def get_delete_url(self):
        return reverse("users:user_delete", kwargs={"pk": self.pk})
    
    def __str__(self) -> str:
        return f'{self.email}'