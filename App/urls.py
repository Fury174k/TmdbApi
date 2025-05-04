from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, RegisterUserView

router = DefaultRouter()
router.register('user-profile', UserProfileViewSet, basename='user-profile')  # Explicitly set basename

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view(), name='register'),
]