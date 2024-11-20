from rest_framework import serializers
from ..models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent', required=False)  # 대댓글의 부모 댓글 필드
    author = serializers.StringRelatedField()  # 작성자 (Profile 모델로부터 직렬화된 닉네임)
    is_private = serializers.BooleanField(default=False)  # 비밀 댓글 여부

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'parent_comment', 'is_private', 'created_at']
