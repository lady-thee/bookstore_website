from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (UserViewset, createView, 
                    loginView, user_logout, 
                    resetPasswordView)


user_router = DefaultRouter()


user_router.register(r"users", UserViewset, basename="user")

urlpatterns = [
    path("", include(user_router.urls)),
    path('create/', createView, name='create'),
    path('login/', loginView, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset-password/', resetPasswordView,name='reset-password'),
]
