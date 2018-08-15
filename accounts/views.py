from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import (
    UserProfileCreateSerializer,
    UserProfileLoginSerializer
)

from rest_framework.permissions import AllowAny

User = get_user_model()


class UserProfileCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileCreateSerializer
    queryset = UserProfile.objects.all()


class UserProfileLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserProfileLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
