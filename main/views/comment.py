from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers.comment import CommentSerializer
from ..models import Post, Comment

# Swagger 요청 및 응답 스키마 정의
comment_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='댓글 내용'),
        'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='비밀 댓글 여부', default=False),
        'parent': openapi.Schema(type=openapi.TYPE_INTEGER, description='대댓글의 부모 댓글 ID', nullable=True),
    },
    required=['content']
)

comment_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='댓글 ID'),
        'author_name': openapi.Schema(type=openapi.TYPE_STRING, description='작성자 이름'),
        'content': openapi.Schema(type=openapi.TYPE_STRING, description='댓글 내용'),
        'is_private': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='비밀 댓글 여부'),
        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description='작성일시'),
        'parent': openapi.Schema(type=openapi.TYPE_INTEGER, description='부모 댓글 ID', nullable=True),
    }
)


class CommentListView(generics.ListCreateAPIView):
    """
    댓글 목록 조회 및 생성
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="댓글 목록 조회 및 생성",
        operation_description="특정 게시판의 특정 게시글에 대한 댓글 목록을 조회하거나 댓글을 생성합니다.",
        request_body=comment_create_request_schema,
        responses={
            200: openapi.Response(description="목록 조회 성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=comment_response_schema
            )),
            201: openapi.Response(description="댓글 생성 성공", schema=comment_response_schema),
            400: openapi.Response(description="잘못된 요청"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        position_id = self.kwargs.get('position_id')
        ftf_id = self.kwargs.get('ftf_id')
        anonymous_id = self.kwargs.get('anonymous_id')
        post_id = self.kwargs.get('post_id')

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

        is_private = self.request.data.get('is_private', False)
        parent_id = self.request.data.get('parent', None)
        parent = None

        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                raise ValidationError({"parent": f"Parent comment with ID {parent_id} not found."})

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

        author_name = self.request.user.profile.nickname
        serializer.save(post=post, author=self.request.user.profile, author_name=author_name, is_private=is_private, parent=parent)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    댓글 상세 조회, 수정 및 삭제
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="댓글 상세 조회, 수정 및 삭제",
        operation_description="특정 댓글의 상세 정보를 조회하거나 내용을 수정 또는 삭제합니다.",
        request_body=comment_create_request_schema,
        responses={
            200: openapi.Response(description="조회 또는 수정 성공", schema=comment_response_schema),
            204: openapi.Response(description="삭제 성공"),
            400: openapi.Response(description="잘못된 요청"),
            404: openapi.Response(description="댓글을 찾을 수 없습니다."),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        position_id = self.kwargs.get('position_id')
        ftf_id = self.kwargs.get('ftf_id')
        anonymous_id = self.kwargs.get('anonymous_id')
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')

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

