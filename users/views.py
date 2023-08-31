import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import UserAccount
from .serializers import LoginSerializer, ResetPasswordSerializer,UpdateUserSerializer, UserSerializer
from .signals import user_created


@api_view(["GET"])
@permission_classes(
    [
        AllowAny,
    ]
)
def listAllUsers(request):
    queryset = UserAccount.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes(
    [
        AllowAny,
    ]
)
def createView(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                user_created.send(
                    sender=settings.AUTH_USER_MODEL,
                    instance=serializer.instance,
                    created=True,
                )
                return Response(
                    {
                        "message": "User successfully created!",
                        "token": str(serializer.instance.auth_token.key),
                    },
                    status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, serializer.errors, status.HTTP_400_BAD_REQUEST
            )

    return Response({"message": "This endpoint handles the creation of users"})


@csrf_exempt
@api_view(["GET", "POST"])
@authentication_classes(
    [
        TokenAuthentication,
        SessionAuthentication,
    ]
)
@permission_classes(
    [
        AllowAny,
    ]
)
def loginView(request):
    if request.method == "POST":
        # logging.debug('Requests: %s', request.data)
        serializer = LoginSerializer(data=request.data, many=False)

        try:
            if serializer.is_valid():
                username_or_email = serializer.validated_data.get("username_or_email")
                password = serializer.validated_data.get("password")
                if username_or_email is None or password is None:
                    raise AuthenticationFailed(
                        "Username or Email and Password required!"
                    )
                else:
                    sym = "@"
                    if sym in username_or_email:
                        user = authenticate(
                            request, email=username_or_email, password=password
                        )
                    else:
                        user = authenticate(
                            request, username=username_or_email, password=password
                        )
                    if user is not None:
                        login(request, user)
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response(
                            {
                                "token": str(token.key),
                                "message": f"{request.user.username} logged in successfully",
                            },
                            status.HTTP_200_OK,
                        )
                        # user_login.send(sender=settings.AUTH_USER_MODEL, request=request, user=request.user)
                    else:
                        raise AuthenticationFailed("Invalid details")
            else:
                return Response(
                    {"error": serializer.errors}, status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            raise AuthenticationFailed("Invalid credentials", str(e))
    return Response(
        {"message": "This endpoint handles the authentication of created users."},
        status.HTTP_200_OK,
    )


@login_required
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"message": "Successfully logged out!"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_200_OK)

    return Response({"message": "This endpoint handles logout integration"})


@login_required
@csrf_exempt
@api_view(["GET", "POST"])
@authentication_classes(
    [
        TokenAuthentication,
        SessionAuthentication,
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def resetPasswordView(request):
    if request.method == "POST":
        serializer = ResetPasswordSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")
            confirm_password = serializer.validated_data.get("confirm_password")
            if not user.check_password(old_password):
                return Response(
                    {"message": "Incorrect password"}, status.HTTP_404_NOT_FOUND
                )
            else:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        {"message": "Password reset successful!"},
                        status.HTTP_202_ACCEPTED,
                    )
                else:
                    return Response({"message": "Passwords mismatch!"})
        else:
            return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)

    return Response({"message": "This endpoint handles the reset password integration"})


@login_required
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieveUserAccountView(request):
    user = request.user
    account = {"id": user.id, "email": user.email, "username": user.username}
    return Response(account, status.HTTP_200_OK)


@login_required
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def updateUserInformation(request):
    user = request.user 
    serializer = UpdateUserSerializer(user, data=request.data)
    if request.method == 'PUT':
        if serializer.is_valid():
            print(user)

            serializer.save()

            return Response({'message': 'Details successfully updated'}, status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': serializer.errors})
    
    return Response({'message': 'This endpoint handles updating user information'}, status.HTTP_200_OK)