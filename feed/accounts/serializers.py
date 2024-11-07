from .models import AuthCode
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise e
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        AuthCode.objects.create(user_id=user)
        return user


class SigninSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def Signin(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if not username or not password:
            raise serializers.ValidationError({"message": "계정과 비밀번호를 입력해주세요."})

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({"message": "계정 또는 비밀번호가 올바르지 않습니다."})
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "username": user.username,
            "refresh": str(refresh),
            "access": str(access),
            }