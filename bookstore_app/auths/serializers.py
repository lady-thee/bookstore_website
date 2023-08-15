from rest_framework import serializers
from .models import Users, Profile


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created_time = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'is_superuser', 'is_active', 'is_verified', 'created_time', 'last_login']

class ProfileSerializer(serializers.ModelSerializer):
    user = UsersSerializer(required=True)

    class Meta:
        model = Profile
        fields = ['user', 'id', 'firstname', 'lastname', 'phone']

    def create(self, validated_data):
        user = UsersSerializer.create(UsersSerializer(), **validated_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile
    
    def update(self, instance, validated_data):
        instance.users = validated_data
        return instance