from django.db import models
class Place(models.Model):
    name = models.CharField(max_length=200)  # 장소 이름
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도
    photo = models.ImageField(upload_to='places/photos/', blank=True, null=True)  # 장소 사진
    opening_hours = models.CharField(max_length=100, blank=True, null=True)  # 영업시간 (예: "09:00 ~ 22:00")

    def __str__(self):
        return self.name
