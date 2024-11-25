from django.db import models
from datetime import datetime
from django.utils.timezone import now


class Cafe(models.Model):
    branch = models.CharField(max_length=100, blank=True, null=True)  # 지점 (예: "서울 강남점")
    name = models.CharField(max_length=200)  # 장소 이름
    address = models.CharField(max_length=300, blank=True, null=True)  # 장소 주소
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도
    photo = models.ImageField(upload_to='places/photos/', blank=True, null=True)  # 장소 사진
    opening_hours = models.CharField(max_length=100, blank=True, null=True)  # 영업시간 (예: "12:00 ~ 22:00")

    def get_status(self):
        """
        현재 시간에 따라 영업 상태 반환:
        - "영업 전"
        - "영업 중"
        - "영업 종료"
        - "영업 시간 정보를 제공해주지 않는 카페입니다."
        """
        if not self.opening_hours:
            return "영업 시간 정보를 제공해주지 않는 카페입니다."

        try:
            start_time, end_time = self.opening_hours.split("~")
            current_time = now().time()
            start_time = datetime.strptime(start_time.strip(), "%H:%M").time()
            end_time = datetime.strptime(end_time.strip(), "%H:%M").time()

            if current_time < start_time:
                return "영업 전"
            elif start_time <= current_time <= end_time:
                return "영업 중"
            else:
                return "영업 종료"
        except ValueError:
            return "영업 시간 정보를 제공해주지 않는 카페입니다."  # 잘못된 형식의 영업 시간도 처리


