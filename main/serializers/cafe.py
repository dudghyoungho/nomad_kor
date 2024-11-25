from rest_framework import serializers
from ..models.cafe import Cafe

class CafeSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField()  # 동적으로 계산되는 필드
    opening_hours = serializers.SerializerMethodField()  # 포맷팅된 영업 시간 필드

    class Meta:
        model = Cafe
        fields = [
            'branch',         # 지점 이름
            'name',           # 장소 이름
            'photo',          # 사진
            'opening_hours',  # 포맷팅된 영업 시간
            'is_open',        # 영업 상태 ("영업 전", "영업 중", "영업 종료")
        ]

    def get_opening_hours(self, obj):
        """
        영업 시간 필드를 "12:00 - 22:00" 형식으로 반환.
        """
        if obj.opening_hours:
            return obj.opening_hours.replace("~", "-")
        return None  # 영업 시간 정보가 없는 경우

    def get_is_open(self, obj):
        """
        현재 영업 상태를 반환.
        """
        return obj.get_status()


