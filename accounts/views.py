from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer
from rest_framework.generics import CreateAPIView


User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

