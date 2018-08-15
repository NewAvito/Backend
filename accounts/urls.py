from django.urls import path

from .views import (
    UserProfileCreateAPIView,
    UserProfileLoginAPIView,
    ChangePasswordAPIView,
    )

urlpatterns = [
    path('login/', UserProfileLoginAPIView.as_view(), name='login'),
    path('register/', UserProfileCreateAPIView.as_view(), name='register'),
    path('password_reset/', ChangePasswordAPIView.as_view(),
         name='password_reset')
]
