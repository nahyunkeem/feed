from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AuthCode

CustomUser = get_user_model()
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        AuthCode.objects.create(user_id=user)
        return user
    
