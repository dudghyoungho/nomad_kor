from rest_framework import serializers
from ..models.cafe import Cafe

class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = [
            'branch',       # 지점 이름
            'name',         # 장소 이름
            'photo',        # 사진
            'opening_hours',# 영업 시간
            'is_open'       # 영업 여부
        ]
