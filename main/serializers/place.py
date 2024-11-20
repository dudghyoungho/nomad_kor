from rest_framework import serializers
from ..models.place import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id',           # 장소 ID
            'name',         # 장소 이름
            'address',      # 장소 주소
            'latitude',     # 위도
            'longitude',    # 경도
            'photo',        # 사진
            'opening_hours',# 영업 시간
            'description',  # 설명
            'reviews'       # 리뷰 데이터 (JSON)
        ]
        read_only_fields = ['id', 'reviews']  # ID와 리뷰는 읽기 전용
