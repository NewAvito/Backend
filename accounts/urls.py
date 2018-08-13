from django.urls import path

from .views import (
    UserProfileCreateAPIView,
    UserProfileLoginAPIView,
    )

urlpatterns = [
    path('login/', UserProfileLoginAPIView.as_view(), name='login'),
    path('register/', UserProfileCreateAPIView.as_view(), name='register'),
]
