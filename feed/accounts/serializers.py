from django.utils import timezone
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AuthCode
from django.contrib.auth.hashers import check_password

CustomUser = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        # 해싱 되지 않는 비밀번호를 삭제하고 해싱시켜 다시 저장
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)       # 비밀번호를 제외한 데이터 
        user.set_password(password)
        user.save()
        
        # 인증 코드 생성
        AuthCode.objects.create(user_id=user)
        return user
    
        # 계정 데이터 인증
    def auth_validate(self, data):
        username = data.get('username')
        password = data.get('password')
        auth_code = data.get('auth_code')

        try:
            user=CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("없는 계정입니다.") 
        
        if not user.check_password(password):
            raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")
        
        

        # 인증 코드 체크
        try:
            auth_code_obj = AuthCode.objects.get(
                user_id=user,
                auth_code=auth_code,
                expired_at__gt=timezone.now()       # 인증 코드가 만료되지 않았나 확인
            )
        except AuthCode.DoesNotExist:
            raise serializers.ValidationError("유효하지 않은 인증 코드입니다.")

        # 인증 완료 후 인증 코드 삭제 
        auth_code_obj.delete()

        user.is_active = True
        user.save()

        return data