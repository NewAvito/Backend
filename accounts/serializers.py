from django.contrib.auth import get_user_model
from .models import UserProfile
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserProfileCreateSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'password',
            'location',
            'mobile',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }
