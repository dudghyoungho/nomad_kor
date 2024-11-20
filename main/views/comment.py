from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from ..models.comment import Comment
from ..models.post import Post
from ..models.profile import Profile
from ..serializers.comment import CommentSerializer


# 댓글 목록 조회 및 작성
class CommentListView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        특정 게시글에 대한 댓글 목록을 반환.
        비밀 댓글은 작성자와 댓글 작성자만 볼 수 있음.
        """
        post_id = self.request.query_params.get('post_id')
        if not post_id:
            return Comment.objects.none()

        queryset = Comment.objects.filter(post_id=post_id, parent=None)

        if self.request.user.is_authenticated:
            post = Post.objects.get(id=post_id)
            queryset = queryset.filter(
                models.Q(is_private=False) |
                models.Q(is_private=True, author__user=self.request.user) |
                models.Q(is_private=True, post__author__user=self.request.user)
            )
        else:
            queryset = queryset.filter(is_private=False)

        return queryset

    def perform_create(self, serializer):
        """
        댓글 작성 로직.
        """
        post_id = self.request.data.get("post_id")
        content = self.request.data.get("content")
        is_private = self.request.data.get("is_private", False)
        parent_comment_id = self.request.data.get("parent_comment_id", None)

        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=self.request.user)
        parent_comment = None
        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        serializer.save(
            post=post,
            author=profile,
            parent=parent_comment,
            is_private=is_private,
            content=content,
        )


# 댓글 상세 조회, 수정, 삭제
class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        댓글 수정 로직.
        """
        content = self.request.data.get("content")
        is_private = self.request.data.get("is_private", False)
        serializer.save(content=content, is_private=is_private)
