from django.urls import path

from users import views



""" URL PATTERNS """

app_name = 'users'

urlpatterns = [
    
    path('users/', views.ListAllAccountAPIView.as_view(), name='users'),
    path('register/', views.AccountRegistrationAPIView.as_view(), name='register'),
    path('login/', views.AccountLoginAPIView.as_view(), name='login'),
    path('logout/', views.AccountLogoutAPIView.as_view(), name='logout'),
    path('reset password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('account settings/', views.RetrieveAccountAPIView.as_view(), name='account_settings'),
    
   
]
