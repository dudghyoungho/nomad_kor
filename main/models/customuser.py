from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# CustomUserManager 정의
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

# CustomUser 모델 정의
class CustomUser(AbstractUser):
    first_name = None  # 불필요한 필드 제거
    last_name = None
    email = None       # 이메일 필드 제거

    objects = CustomUserManager()  # CustomUserManager 연결

    def __str__(self):
        return self.username

