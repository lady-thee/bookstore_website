from django.urls import path

from .views import (
    createView,
    listAllUsers,
    loginView,
    resetPasswordView,
    retrieveUserAccountView,
    updateUserInformation,
    user_logout,
)

urlpatterns = [
    path("", listAllUsers),
    path("create/", createView, name="create"),
    path("login/", loginView, name="login"),
    path("logout/", user_logout, name="logout"),
    path("reset-password/", resetPasswordView, name="reset-password"),
    path("account/", retrieveUserAccountView, name='account'),
    path("update/", updateUserInformation, name="update"),
]
