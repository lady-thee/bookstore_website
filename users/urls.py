from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateUserView, LoginUserView, UserViewset

# class CustomRouter(DefaultRouter):
#     routes = []

user_router = DefaultRouter()
create_router = DefaultRouter()
login_router = DefaultRouter()

user_router.register(r"users", UserViewset, basename="user")
create_router.register(r"create", CreateUserView, basename="create")
login_router.register(r"", LoginUserView, basename="login")

urlpatterns = [
    path("", include(user_router.urls)),
    path("", include(create_router.urls)),
    path("", include(login_router.urls)),
]
