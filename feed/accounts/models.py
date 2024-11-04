from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField("email address", unique=True)
    first_name = None
    last_name = None
    is_active = models.BooleanField(default=False)


class AuthCode(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expired_at = timezone.now() + timedelta(days=1)
        self.auth_code = random.randint(100000, 999999)
        # print(self.auth_code)
        super().save(*args, **kwargs)