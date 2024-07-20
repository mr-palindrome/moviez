from typing import Dict, Any

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class RegisterUserSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]):
        username = attrs.get("username")
        password = attrs.get("password")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists with this username!")

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        return super().validate(attrs)


class LoginUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("No active account found with the given credentials")
        self.user = user
        return super().validate(attrs)