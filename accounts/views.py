from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from .models import UserProfile
from .serializers import UserProfileCreateSerializer


User = get_user_model()


class UserProfileCreateAPIView(CreateAPIView):
    serializer_class = UserProfileCreateSerializer
    queryset = UserProfile.objects.all()

