from rest_framework import serializers
from .models import Users, Profile

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # user = UsersSerializer(required=True)

    class Meta:
        model = Profile
        fields = ['user', 'id', 'firstname', 'lastname', 'phone']

    
 
class UsersSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    profile = ProfileSerializer(required=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password', 'is_superuser', 'is_active', 'is_verified', 'created_time', 'last_login', 'profile']

