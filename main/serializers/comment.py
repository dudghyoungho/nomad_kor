from rest_framework import serializers
from ..models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)  # 댓글 작성자의 닉네임
    parent_id = serializers.IntegerField(source='parent.id', read_only=True)  # 부모 댓글 ID
    is_private = serializers.BooleanField(read_only=True)  # 비밀 댓글 여부

    class Meta:
        model = Comment
        fields = ['id','author_nickname', 'content', 'parent_id', 'is_private', 'created_at']

