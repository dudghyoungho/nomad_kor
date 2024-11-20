from rest_framework import serializers
from ..models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'age', 'gender']

    def validate_nickname(self, value):
        """닉네임 중복 검사"""
        if Profile.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def validate_age(self, value):
        """나이 유효성 검사"""
        if value < 0:
            raise serializers.ValidationError("나이는 양수여야 합니다.")
        return value

    def validate_gender(self, value):
        """성별 유효성 검사"""
        if value not in ['M', 'F']:
            raise serializers.ValidationError("성별은 'M'(남성) 또는 'F'(여성)만 입력 가능합니다.")
        return value

