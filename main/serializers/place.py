from rest_framework import serializers
from ..models.place import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'branch',       # 지점 이름
            'name',         # 장소 이름
            'photo',        # 사진
            'opening_hours',# 영업 시간
            'is_open'       # 영업 여부
        ]
