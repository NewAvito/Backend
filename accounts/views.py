from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import (
    UserProfileCreateSerializer,
    UserProfileLoginSerializer,
    ChangePasswordSerializer
)

from rest_framework.permissions import AllowAny, IsAuthenticated

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


class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = UserProfile
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("password")
            if not obj.check_password(old_password):
                return Response({"password": ["Wrong password."]},
                                status=HTTP_400_BAD_REQUEST)
            obj.set_password(serializer.data.get("new_password"))
            obj.save()
            return Response("Your password is changed.", status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
