from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'signup', views.AppCreate)

urlpatterns = [
    path('', views.apiOverview),
    # path('signup/', views.AppCreate.as_view()),
    path('', include(router.urls)),
    path('users/', views.AppList.as_view()),
]