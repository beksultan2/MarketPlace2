from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "username", "email", "phone_number", "age", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password2"):
            raise serializers.ValidationError({"password2": "Сырсөздөр дал келген жок"})
        return attrs

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Логин же сырсөз туура эмес")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт активдүү эмес")
        attrs["user"] = user
        return attrs

    def to_representation(self, instance):
        user = instance["user"]
        refresh = RefreshToken.for_user(user)
        return {
            "user": UserProfileSerializer(user, context=self.context).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "username", "email", "first_name", "last_name",
                  "phone_number", "avatar", "age")
        read_only_fields = ("id",)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
