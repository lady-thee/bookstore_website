from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import PasswordResetView
from .views import UserViewset,createView, loginView, user_logout

# class CustomRouter(DefaultRouter):
#     routes = []

user_router = DefaultRouter()
create_router = DefaultRouter()
login_router = DefaultRouter()
reset_router = DefaultRouter()

user_router.register(r"users", UserViewset, basename="user")
# create_router.register(r"create", CreateUserView, basename="create")
# login_router.register(r"", LoginUserView, basename="login")
# reset_router.register(r"reset", UpdatePasswordView, basename='reset-password')

urlpatterns = [
    path("", include(user_router.urls)),
    path('create/', createView, name='create'),
    path('login/', loginView, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]
