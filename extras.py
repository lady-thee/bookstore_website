from dataclasses import dataclass


@dataclass
class NewPerson:
    name: str
    age: int
    city: str


p = NewPerson("Nobara", 23, "japan")
print(p)
print(p.name, p.age)

print(hash(p))

{
    "email": "theolam6@gmail.com",
    "password": "2030",
    "username": "theola"
}

{
  "username_or_email": "theolam6@gmail.com",
  "password": "2030"
}

{
   "username_or_email": "theola",
   "password": "2030"
}

{
   "old_passwordl": "2030",
   "new_password": "apple",
   "confirm_password": "apple"
}

# {"username_or_email": "theolam6@gmail.com", "password": "2030"}

  # path("", include(create_router.urls)),
    # path("", include(login_router.urls)),
    # path("reset/", include(reset_router.urls)),
    # path('reset/', reset_password, name='reset'),
    
# class CreateUserView(viewsets.ModelViewSet):
#     permission_classes = (AllowAny,)
#     authentication_classes = (TokenAuthentication, SessionAuthentication,)
#     serializer_class = UserSerializer
#     queryset = UserAccount.objects.all()
    
  
#     def create(self, request):
#         pdb.run()
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer) 

#         try:
#             user_created.send(sender=settings.AUTH_USER_MODEL, instance=serializer.instance, created=True)
#             headers = self.get_success_headers(serializer.data)

#             return Response({'message': 'Created successfully!'}, status.HTTP_201_CREATED, headers=headers)
#         except Exception as e:
#             return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
#     # @csrf_exempt
    # def create(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         try:
    #             user = serializer.save()
    #             token, _ = Token.objects.get_or_create(user=user)
    #             return Response({"token": str(token.key)}, status=status.HTTP_201_CREATED)
    #         except IntegrityError:
    #             raise ValidationError("Username or email already exists.")
    #     else:
    #         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# class LoginUserView(viewsets.ViewSet):
#     permission_classes = [AllowAny]
#     # authentication_classes = []
#     @csrf_exempt
#     @action(methods=["post"], detail=False)
#     def login(self, request):
#         print(request.user)
#         if request.method == "POST":
#             data = JSONParser().parse(request)
#             username_or_email = data["username_or_email"]
#             password = data["password"]

#             if username_or_email is None or password is None:
#                 print({"email/username": username_or_email, "password": password})
#                 raise AuthenticationFailed("Username or email and password is required")

#             else:
#                 pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

#                 if re.match(pattern, username_or_email):
#                     user = authenticate(email=username_or_email, password=password)
#                     login(request, user)
#                 else:
#                     user = authenticate(email=username_or_email, password=password)
#                     login(request, user)
#                 if user is None:
#                     raise AuthenticationFailed("Invalid details")
#                 else:
#                     token, _ = Token.objects.get_or_create(user=user)
#                     return Response(
#                         {"user_id": user.id, "token": str(token.key)}, status.HTTP_200_OK
#                     )

                    # sym = '@'
                    # if sym in username_or_email:
                    #     user = authenticate(request, username=username_or_email, password=password)
                    #     if user is not None:
                    #         login(request, user)
                    #         user_login.send(sender=settings.AUTH_USER_MODEL, request=request, user=request.user)
                    #     else:
                    #         raise AuthenticationFailed("Invalid details")
                    # else:
                    #     user = authenticate(request, username=username_or_email, password=password)
                    #     if user is not None:
                    #         login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                    #         user_login.send(sender=settings.AUTH_USER_MODEL, request=request, user=request.user)
                    #     else:
                    #         raise AuthenticationFailed("Invalid details")
                    
                        # if Token.objects.get(user=request.user):
                        #     print({'message': Token.objects.get(user=request.user)})
                        # else:
                        #     print('No token generated for this user')

# @permission_classes([IsAuthenticated])
# @csrf_exempt
# @api_view(['POST'])
# def reset_password(request):
#     serializer = ResetPasswordSerializer(data=JSONParser().parse(request))
#     if serializer.is_valid():
#         user = request.user
#         if user.check_password(serializer.validated_data.get('old_password')):
#             user.set_password(serializer.validated_data.get('new_password'))
#             user.save()
#             update_session_auth_hash(request, user)
#             return Response({
#                         'message': 'Password reset successful!'
#                     }, status.HTTP_200_OK)
#         else:
#             return Response({
#                 'message': 'Incorrect old password'
#             }, status.HTTP_400_BAD_REQUEST)
    
        
# def login_user(sender, request, user, **kwargs):


# user_login.connect(login_user, sender=settings.AUTH_USER_MODEL)
# @receiver(user_created, sender=settings.AUTH_USER_MODEL)
# def send_welcome_mail(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Welcome to Ikenga'
#         body = render_to_string(
#             'welcome.html',
#             {
#                 'user': instance,
#             }
#         )
#         email = EmailMessage(
#             subject= subject,
#             body=body,
#             from_email=settings.EMAIL_HOST_USER,
#             to=[instance.email]
#         )
#         email.content_subtype = 'html'
#         email.send()

# welcome_email.connect(send_welcome_mail, sender=settings.AUTH_USER_MODEL)

# request.auth.delete()
# request.session.flush()

# create_router.register(r"create", CreateUserView, basename="create")
# login_router.register(r"", LoginUserView, basename="login")
# reset_router.register(r"reset", UpdatePasswordView, basename='reset-password')
