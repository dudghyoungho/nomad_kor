from django.contrib.auth.models import AbstractUser
from django.db import models
#유저
class CustomUser(AbstractUser):
    # Django 기본 AbstractUser를 활용
    first_name = None  # 불필요한 필드 제거
    last_name = None
    email = None       # 필요 시 추가 가능

    def __str__(self):
        return self.username
