from rest_framework import serializers
from ..models.rating import Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 작성자 이름 읽기 전용
    cafe = serializers.ReadOnlyField(source='cafe.name')    # 장소 이름 읽기 전용

    class Meta:
        model = Rating
        fields = ['id', 'user', 'cafe', 'rating', 'created_at']  # 포함할 필드
        read_only_fields = ['created_at']  # 작성 시간은 읽기 전용
