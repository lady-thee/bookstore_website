import re 

from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import Account





""" Serializers are initialised here  """

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = Account
        exclude = ('id', 'is_active', 'is_superuser', 'is_staff', 'created_time', 'last_login', 'is_verified', 'groups', 'user_permissions')


    def validate_email(self, email):
        pattern = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        
        if re.match(pattern, email):
            if Account.objects.filter(email=email).exists():
                raise serializers.ValidationError('Email already exists!')
            return email
        raise serializers.ValidationError('Invalid email format!')
    
    
    def create(self, validated_data):
        password = self.validated_data.get('password')
        # pattern = r'!@#$%&\^*(),.?":{}|<>'
        
        error_messages = []
        
        # if not re.search(pattern, password):
        #         error_messages.append(f'Passwords must contain at least one SPECIAL characters {pattern}')
            
        try: 
            validate_password(password)   
        except serializers.ValidationError as e:
            error_messages.append(str(e))
        
        if error_messages:
            raise serializers.ValidationError(error_messages)
        
        user = Account.objects.create_user(**validated_data)
        return user


class ListAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        pattern = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        username_or_email = data.get('username_or_email')
        password = data.get('password')
        
        if re.match(pattern, username_or_email):
            try:
                user = Account.objects.get(email=username_or_email)
                username_or_email_field = 'email'
            except Account.DoesNotExist:
                raise serializers.ValidationError('Account with Email does not exist!')
        else:
            try:
                user = Account.objects.get(username=username_or_email)
                username_or_email_field = 'username'
            except Account.DoesNotExist:
                raise serializers.ValidationError('Account with Username does not exist!')
        
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password!')
        
        data['user'] = user
        data['username_or_name'] = username_or_email_field
        return data
        




class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def get_user(self):
        request = self.context['request']
        user = request.user
        return user
    
    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        user = self.get_user()
        
        if not user.check_password(old_password):
            raise serializers.ValidationError('Password Incorrect!')
        
        try:
            # pattern = r'!@#$%&\^*(),.?":{}|<>'
        
            error_messages = []
  
            try: 
                validate_password(new_password)   
            except serializers.ValidationError as e:
                error_messages.append(str(e))
            
            if error_messages:
                raise serializers.ValidationError(error_messages)
            if new_password != confirm_password:
                raise serializers.ValidationError(f'{new_password} and {confirm_password} do not match')
            
        except serializers.ValidationError as e:
            raise serializers.ValidationError('Password invalid!')
           
        return data
    
    def save(self, **kwargs):
        user = self.get_user()
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user 
        
                
        
class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('id', 'is_active', 'is_superuser', 'is_staff', 'created_time', 'password', 
                   'last_login', 'is_verified', 'groups', 'user_permissions')
