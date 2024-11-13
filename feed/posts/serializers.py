from rest_framework import serializers
from feed.accounts import models
from .models import Post
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

