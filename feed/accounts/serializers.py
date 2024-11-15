from .models import AuthCode
from django.utils import timezone
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        
        AuthCode.objects.create(user_id=user)
        return user

    def update(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        auth_code = validated_data.get('auth_code')

        try:
            user=CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"message": "없는 계정입니다."}) 
        
        if not user.check_password(password):
            raise serializers.ValidationError({"message": "비밀번호가 올바르지 않습니다."})
        
        try:
            auth_code_obj = AuthCode.objects.get(
                user_id=user,
                auth_code=auth_code,
                expired_at__gt=timezone.now()
            )
        except AuthCode.DoesNotExist:
            raise serializers.ValidationError({"message": "유효하지 않은 인증 코드입니다."})

        auth_code_obj.delete()

        user.is_active = True
        user.save()

        return user


class SigninSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["username"] = self.user.username
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data