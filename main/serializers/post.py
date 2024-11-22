# serializers/post.py
from rest_framework import serializers
from ..models import Post

class PostSerializer(serializers.ModelSerializer):
    board = serializers.ReadOnlyField(source='board.id')  # board 필드를 읽기 전용으로 설정
    author = serializers.ReadOnlyField(source='author.nickname')  # 클라이언트가 제공하지 않아도 됨

    class Meta:
        model = Post
        fields = ['id', 'board', 'author', 'title', 'content', 'created_at']

