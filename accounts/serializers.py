from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import UserProfile
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField
)

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

    def validate(self, data):
        mobile = data['mobile']
        user_qs = UserProfile.objects.filter(mobile=mobile)
        if user_qs.exists():
            raise ValidationError("A user with that mobile number"
                                  " already exists.")
        return data

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


class UserProfileLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=True, allow_blank=False)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        username = data.get("username")
        password = data.get("password")
        if not username:
            raise ValidationError("A username is required to login.")

        user = User.objects.filter(Q(username=username)).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Not valid username")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Not valid password")

        return data
