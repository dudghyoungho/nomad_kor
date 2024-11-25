from django.db import models

class Cafe(models.Model):
    branch = models.CharField(max_length=100, blank=True, null=True)  # 지점 (예: "서울 강남점")
    name = models.CharField(max_length=200)  # 장소 이름
    address = models.CharField(max_length=300, blank=True, null=True)  # 장소 주소
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도
    photo = models.ImageField(upload_to='places/photos/', blank=True, null=True)  # 장소 사진
    opening_hours = models.CharField(max_length=100, blank=True, null=True)  # 영업시간 (예: "09:00 ~ 22:00")
    is_open = models.BooleanField(default=False)  # 영업 여부 (True: 영업 중, False: 영업 중 아님)

    def __str__(self):
        return f"{self.branch} - {self.name}" if self.branch else self.name

