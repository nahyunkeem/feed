from rest_framework import serializers
from feed.accounts import models
from .models import Like, Post
from django.db import models
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    # 모든 타입 정의 
    class AllType(models.TextChoices):
        FACEBOOK = 'facebook', 'Facebook'
        TWITTER = 'twitter', 'Twitter'
        INSTAGRAM = 'instagram', 'Instagram'
        THREADS = 'threads', 'Threads'

    type = serializers.ChoiceField(choices=AllType.choices)
    

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


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content_id', 'type', 'title', 'content', 
                'view_count', 'like_count', 'share_count', 'created_at', 
                'updated_at']


# 게시물 좋아요 (목록. 상세)
class PostLikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['user_id', 'post_id', 'is_like','created_at']
        read_only_fields = ['created_at']

