
from django.contrib.auth import  login, logout

from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Account
from .serializers import (
    AccountSettingsSerializer,
    ListAccountsSerializer,
    LoginSerializer,
    UserSerializer,
    ResetPasswordSerializer,
)
from .signals import user_created


"""API endpoints using Class Base Views"""

class ListAllAccountAPIView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = ListAccountsSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAdminUser]

class AccountRegistrationAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        user_created.send(sender=user.__class__, instance=user)
        return Response({'message': 'User Created Successfully!', 'account': UserSerializer(user).data}, status.HTTP_201_CREATED)
        
     
    
class AccountLoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user, backend="users.backends.EmailorUsernameModelBackend")
            
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'User Logged in Successfully!', 'token': token.key}, status=status.HTTP_200_OK)
        
        
class AccountLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    def post(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"message": "Successfully logged out!"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_200_OK)
    # def get(self, request):
    #     target_url = reverse('login')
    #     return HttpResponseRedirect(target_url)


class ResetPasswordAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    serializer_class = ResetPasswordSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        Token.objects.get_or_create(user=user)
        return Response({'message': 'Password Reset Successful!'}, status.HTTP_200_OK)
    
    

class RetrieveAccountAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSettingsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    
    def get_object(self):
        if not self.request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user_email = self.request.user.email 
        user_id = Account.objects.filter(email=user_email).values_list('id', flat=True).get()
        obj = Account.objects.get(id=user_id)
        self.check_object_permissions(self.request, obj)
        return obj 
        
    
    def get(self, request, *args,  **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        account = self.get_object()
        serializer = self.get_serializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Details Updated Successfully!', 'detail': serializer.data}, status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        account = self.get_object()
        account.delete()
        return Response({'message': 'Account Successfully Deleted!'}, status.HTTP_204_NO_CONTENT)