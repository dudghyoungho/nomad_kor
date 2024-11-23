from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from ..models import Post, Comment
from ..serializers.comment import CommentSerializer
from django.http import Http404

class IsAuthorOrPostAuthorPermission(BasePermission):
    """
    댓글 작성자만 댓글 수정 및 삭제 가능. 비밀 댓글/대댓글은 게시글 작성자와 댓글 작성자만 볼 수 있음.
    """
    def has_object_permission(self, request, view, obj):
        # 수정 및 삭제 권한: 댓글 작성자나 게시글 작성자
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user.profile or obj.post.author == request.user.profile

        # 조회 권한: 비밀 댓글은 게시글 작성자와 댓글 작성자만 조회 가능
        if obj.is_private:
            return obj.author == request.user.profile or obj.post.author == request.user.profile

        return True

class CommentListView(generics.ListCreateAPIView):
    """
    댓글 목록 조회 및 생성
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # URL에서 position_id, ftf_id, anonymous_id, post_id 가져오기
        position_id = self.kwargs.get('position_id')
        ftf_id = self.kwargs.get('ftf_id')
        anonymous_id = self.kwargs.get('anonymous_id')
        post_id = self.kwargs.get('post_id')

        # 각 게시판에서의 Post를 필터링
        if position_id:
            try:
                post = Post.objects.get(position_id=position_id, id=post_id)
                return Comment.objects.filter(post=post)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for position_id {position_id}."})

        elif ftf_id:
            try:
                post = Post.objects.get(ftf_id=ftf_id, id=post_id)
                return Comment.objects.filter(post=post)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for ftf_id {ftf_id}."})

        elif anonymous_id:
            try:
                post = Post.objects.get(anonymous_id=anonymous_id, id=post_id)
                return Comment.objects.filter(post=post)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for anonymous_id {anonymous_id}."})

        raise ValidationError({"error": "Invalid board or post."})

    def perform_create(self, serializer):
        position_id = self.kwargs.get('position_id')
        ftf_id = self.kwargs.get('ftf_id')
        anonymous_id = self.kwargs.get('anonymous_id')
        post_id = self.kwargs.get('post_id')

        # 비밀 댓글 여부 확인 (기본값은 False)
        is_private = self.request.data.get('is_private', False)

        # parent 필드를 확인하여 대댓글인지 판단
        parent_id = self.request.data.get('parent', None)
        parent = None

        if parent_id:  # 대댓글인 경우
            parent = Comment.objects.get(id=parent_id)
            is_private = True  # 대댓글은 기본적으로 비밀 댓글

        # 게시글 찾기
        if position_id:
            try:
                post = Post.objects.get(position_id=position_id, id=post_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for position_id {position_id}."})
        elif ftf_id:
            try:
                post = Post.objects.get(ftf_id=ftf_id, id=post_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for ftf_id {ftf_id}."})
        elif anonymous_id:
            try:
                post = Post.objects.get(anonymous_id=anonymous_id, id=post_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for anonymous_id {anonymous_id}."})
        else:
            raise ValidationError({"error": "Invalid board type in URL."})

        # 익명 게시판인 경우 author_name을 "익명"으로 설정
        if 'anonymous' in self.request.path:
            author_name = "익명"
        else:
            author_name = self.request.user.profile.nickname  # 프로필의 nickname 사용

        # 댓글 저장
        serializer.save(post=post, author=self.request.user.profile, author_name=author_name,
                        is_private=is_private, parent=parent)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    댓글 상세 조회, 수정 및 삭제
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrPostAuthorPermission]

    def get_object(self):
        position_id = self.kwargs.get('position_id')
        ftf_id = self.kwargs.get('ftf_id')
        anonymous_id = self.kwargs.get('anonymous_id')
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')

        # Position, FTF, Anonymous board에서의 Post를 필터링
        if position_id:
            try:
                post = Post.objects.get(position_id=position_id, id=post_id)
                return Comment.objects.get(post=post, id=comment_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for position_id {position_id}."})
            except Comment.DoesNotExist:
                raise ValidationError({"comment": f"Comment with ID {comment_id} not found."})

        elif ftf_id:
            try:
                post = Post.objects.get(ftf_id=ftf_id, id=post_id)
                return Comment.objects.get(post=post, id=comment_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for ftf_id {ftf_id}."})
            except Comment.DoesNotExist:
                raise ValidationError({"comment": f"Comment with ID {comment_id} not found."})

        elif anonymous_id:
            try:
                post = Post.objects.get(anonymous_id=anonymous_id, id=post_id)
                return Comment.objects.get(post=post, id=comment_id)
            except Post.DoesNotExist:
                raise ValidationError({"post": f"Post not found for anonymous_id {anonymous_id}."})
            except Comment.DoesNotExist:
                raise ValidationError({"comment": f"Comment with ID {comment_id} not found."})

        raise ValidationError({"error": "Invalid board type or post in URL."})
