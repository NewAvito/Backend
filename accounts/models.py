from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    location = models.CharField(max_length=30, blank=True)
    mobile = models.IntegerField()
