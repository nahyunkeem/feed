from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

CustomUser = get_user_model()


class Post(models.Model):
    content_id = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=50)


class PostHashtag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag_id = models.ForeignKey(Hashtag, on_delete=models.CASCADE)


class Like(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

