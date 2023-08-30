import datetime

from rest_framework import serializers

from .models import UserAccount


class UserSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(source="is_active", default=True)
    verified = serializers.BooleanField(source="is_verified", default=False)
    superuser = serializers.BooleanField(source="is_superuser", default=False)
    staff = serializers.BooleanField(source="is_staff", default=False)

    class Meta:
        model = UserAccount
        fields = [
            "id",
            "email",
            "username",
            "password",
            "active",
            "verified",
            "superuser",
            "staff",
            "created_time",
            "last_login",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data["is_active"] = True
        user = UserAccount.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = ['username_or_email', 'password']
        

class ResetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
       fields = ['']
        