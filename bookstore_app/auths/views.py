from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import IntegrityError, InternalError

from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import Users, Profile
from .serializers import UsersSerializer, ProfileSerializer


def loadSignUpView(request):
    return HttpResponse('Sign Up Page')


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Users': '/users/',
        'Sign up': '/signup/',
        'Log in': '/login/',
    }
    return Response(api_urls)
    

class AppList(generics.ListAPIView):
     queryset = Users

     def get(self, request, format=None):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    

class AppCreate(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    # serializer_class = ProfileSerializer
    queryset = Users.objects.all()

    

    # queryset = Profile.objects.all()
    
    # @csrf_exempt
    # def post(self, request, format=None):
    #     if request.method == 'POST':
    #         try:
    #             data = JSONParser().parse(request)
    #             user = Users.objects.create_user(email=data['email'], password=data['password'])
    #             profile = Profile.objects.create(user=user, firstname=data['firstname'], lastname=data['lastname'], phone=data['phone'])
    #             profile.save()

    #             return Response('Saved successfully', status=200)
    #         except (IntegrityError, InternalError):
    #             return Response('Email already exists', status=400)


