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
        ("ST", "창업가"),
        ("CT", "크리에이터"),
        ("MK", "마케터"),
    ]
    AREA_CHOICES = [
        ("서울특별시 종로구", "서울특별시 종로구"),
        ("서울특별시 중구", "서울특별시 중구"),
        ("서울특별시 용산구", "서울특별시 용산구"),
        ("서울특별시 성동구", "서울특별시 성동구"),
        ("서울특별시 광진구", "서울특별시 광진구"),
        ("서울특별시 동대문구", "서울특별시 동대문구"),
        ("서울특별시 중랑구", "서울특별시 중랑구"),
        ("서울특별시 성북구", "서울특별시 성북구"),
        ("서울특별시 강북구", "서울특별시 강북구"),
        ("서울특별시 도봉구", "서울특별시 도봉구"),
        ("서울특별시 노원구", "서울특별시 노원구"),
        ("서울특별시 은평구", "서울특별시 은평구"),
        ("서울특별시 서대문구", "서울특별시 서대문구"),
        ("서울특별시 마포구", "서울특별시 마포구"),
        ("서울특별시 양천구", "서울특별시 양천구"),
        ("서울특별시 강서구", "서울특별시 강서구"),
        ("서울특별시 구로구", "서울특별시 구로구"),
        ("서울특별시 금천구", "서울특별시 금천구"),
        ("서울특별시 영등포구", "서울특별시 영등포구"),
        ("서울특별시 동작구", "서울특별시 동작구"),
        ("서울특별시 관악구", "서울특별시 관악구"),
        ("서울특별시 서초구", "서울특별시 서초구"),
        ("서울특별시 강남구", "서울특별시 강남구"),
        ("서울특별시 송파구", "서울특별시 송파구"),
        ("서울특별시 강동구", "서울특별시 강동구"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    job = models.CharField(max_length=2, choices=JOB_CHOICES)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)  # 'area' 필드 추가
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nickname
