from rest_framework import serializers
from .models import Post, Hashtag

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
        model = Post, Hashtag
        fields = [
            'hashtag',
            'type',
        ]
