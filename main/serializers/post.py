# serializers/post.py
from rest_framework import serializers
from ..models import Post

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)  # nickname을 가져옵니다.

    class Meta:
        model = Post
        fields = ['id', 'author','author_nickname', 'title', 'content', 'image', 'created_at']  # 불필요한 필드 제외


