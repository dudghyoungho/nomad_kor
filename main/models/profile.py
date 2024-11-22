from django.conf import settings
from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
    ]

    JOB_CHOICES = [
        ("FE", "프론트엔드 개발자"),
        ("BE", "백엔드 개발자"),
        ("PM", "기획자"),
        ("DS", "디자이너"),
        ("BL", "블로거"),
        ("MK", "마케터"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # max_length=1로 변경
    job = models.CharField(max_length=2, choices=JOB_CHOICES)  # 직군 필드 추가
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nickname


