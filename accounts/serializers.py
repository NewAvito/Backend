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

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        location = validated_data['location']
        mobile = validated_data['mobile']
        user_obj = UserProfile(
            username=username,
            location=location,
            mobile=mobile,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
