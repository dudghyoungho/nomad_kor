from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import Post, Comment
from ..serializers.comment import CommentSerializer
from rest_framework.permissions import BasePermission


class IsAuthorOrPostAuthorPermission(BasePermission):
    """
    댓글 작성자만 댓글 수정 및 삭제 가능. 또한, 비밀 댓글은 게시글 작성자와 댓글 작성자만 볼 수 있음.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user.profile or obj.post.author == request.user.profile
        return True


class CommentListView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)

        # 비밀 댓글을 작성자와 게시글 작성자만 볼 수 있도록 필터링
        if self.request.user.profile == post.author:
            return Comment.objects.filter(post=post)
        return Comment.objects.filter(post=post, is_private=False)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)

        # 비밀 댓글 여부 설정
        is_private = self.request.data.get('is_private', False)

        # 대댓글일 경우, parent 필드 설정
        parent_comment = self.request.data.get('parent', None)
        if parent_comment:
            parent_comment = Comment.objects.get(id=parent_comment)

        # 댓글 생성
        comment = serializer.save(
            post=post,
            author=self.request.user.profile,  # 로그인한 사용자의 프로필을 author로 설정
            is_private=is_private,
            parent=parent_comment if parent_comment else None  # 대댓글일 경우 parent 설정
        )
        return comment


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrPostAuthorPermission]

    def get_object(self):
        obj = super().get_object()
        # 비밀 댓글에 대한 권한 체크
        if obj.is_private and obj.author != self.request.user.profile and obj.post.author != self.request.user.profile:
            raise PermissionDenied("You do not have permission to view this comment.")
        return obj

