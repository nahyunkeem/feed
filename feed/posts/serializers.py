from rest_framework import serializers
from .models import Post, Hashtag
from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'type',
            'title',
            'content',
        ]


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at']

