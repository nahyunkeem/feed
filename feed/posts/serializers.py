from .models import Post
from django.contrib.auth import get_user_model
from rest_framework import serializers

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at']