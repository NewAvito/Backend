from django.urls import path

from .views import (
    UserProfileCreateAPIView,
    )

urlpatterns = [
    path('register/', UserProfileCreateAPIView.as_view(), name='register'),
]
