from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserAccount
from .serializers import UserSerializer

import re 


class UserViewset(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = UserAccount.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data) 


class CreateUserView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @csrf_exempt
    # @action(methods=['post'], detail=False)
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                token = Token.objects.get_or_create(user=user)
                return Response({
                    'token': str(token)
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                raise ValidationError('Username or email already exists.')
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

class LoginUserView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def login(self, request):
        if request.method == 'POST':
            data = JSONParser().parse(request)
            username_or_email = data['username_or_email']
            password = data['password']

            if username_or_email is None or password is None:
                print({'email/username': username_or_email, 'password': password})
                raise AuthenticationFailed('Username or email and password is required')
                
            else:
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                if re.match(pattern, username_or_email):
                    user = authenticate(email=username_or_email, password=password)
                    login(request, user)
                else:
                    user = authenticate(email=username_or_email, password=password)
                    login(request, user)
                if user is None:
                    raise AuthenticationFailed('Invalid details')
                else:
                    token = Token.objects.get_or_create(user=user)
                    return Response({
                        'user_id': user.id,
                        'token': str(token)
                    }, status.HTTP_200_OK)

       


        