from rest_framework import serializers
from ..models.review import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 사용자 이름을 문자열로 반환
    cafe = serializers.PrimaryKeyRelatedField(read_only=True)  # 장소 ID만 반환

    class Meta:
        model = Review
        fields = ['id', 'user', 'cafe', 'content', 'created_at', 'updated_at']  # 필요한 필드만 포함
