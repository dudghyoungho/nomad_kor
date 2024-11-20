from django.conf import settings
from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "남성"),
        ("F", "여성"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # max_length=1로 변경
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nickname

