from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers.post import PostSerializer
from ..models import Position, FTF, Anonymous, Post

class PostListView(ListCreateAPIView):
    """
    게시글 목록 조회 및 생성
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Swagger 요청 및 응답 스키마 정의
    post_create_request_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 제목'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 내용'),
            'image': openapi.Schema(type=openapi.TYPE_STRING, format='binary', description='첨부 이미지 (선택)'),
        },
        required=['title', 'content']
    )

    post_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='게시글 ID'),
            'author_name': openapi.Schema(type=openapi.TYPE_STRING, description='작성자 이름'),
            'title': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 제목'),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description='게시글 내용'),
            'image': openapi.Schema(type=openapi.TYPE_STRING, description='첨부 이미지 URL'),
            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description='작성일시'),
        }
    )

    @swagger_auto_schema(
        operation_summary="게시글 목록 조회",
        operation_description="특정 게시판의 게시글 목록을 반환합니다.",
        responses={
            200: openapi.Response(description="성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=post_response_schema
            ))
        }
    )
    @swagger_auto_schema(
        operation_summary="게시글 생성",
        operation_description="특정 게시판에 새로운 게시글을 생성합니다.",
        request_body=post_create_request_schema,
        responses={
            201: openapi.Response(description="게시글 생성 성공", schema=post_response_schema),
            400: openapi.Response(description="잘못된 요청"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        path = self.request.path

        if 'position' in path:
            position_id = self.kwargs.get('position_id')
            if not position_id:
                raise ValidationError({"position": "Position ID is missing from the request URL."})

            try:
                position = Position.objects.get(id=position_id)
            except Position.DoesNotExist:
                raise ValidationError({"position": f"Position with the given ID {position_id} does not exist."})

            serializer.save(position=position, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

        elif 'ftf' in path:
            ftf_id = self.kwargs.get('ftf_id')
            if not ftf_id:
                raise ValidationError({"ftf": "FTF ID is missing from the request URL."})

            try:
                ftf = FTF.objects.get(id=ftf_id)
            except FTF.DoesNotExist:
                raise ValidationError({"ftf": f"FTF with the given ID {ftf_id} does not exist."})

            serializer.save(ftf=ftf, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

        elif 'anonymous' in path:
            anonymous_id = self.kwargs.get('anonymous_id')
            if not anonymous_id:
                raise ValidationError({"anonymous": "Anonymous ID is missing from the request URL."})

            try:
                anonymous = Anonymous.objects.get(id=anonymous_id)
            except Anonymous.DoesNotExist:
                raise ValidationError({"anonymous": f"Anonymous board with the given ID {anonymous_id} does not exist."})

            serializer.save(anonymous=anonymous, author=self.request.user.profile, author_name="익명")

        else:
            raise ValidationError({"error": "Invalid board type in URL."})


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """
    게시글 상세 조회, 수정 및 삭제
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시글 상세 조회",
        operation_description="특정 게시판의 특정 게시글을 조회합니다.",
        responses={
            200: openapi.Response(description="성공", schema=post_response_schema),
            404: openapi.Response(description="게시글을 찾을 수 없습니다."),
        }
    )
    @swagger_auto_schema(
        operation_summary="게시글 수정",
        operation_description="특정 게시글의 정보를 수정합니다.",
        request_body=post_create_request_schema,
        responses={
            200: openapi.Response(description="수정 성공", schema=post_response_schema),
            400: openapi.Response(description="잘못된 요청"),
            404: openapi.Response(description="게시글을 찾을 수 없습니다."),
        }
    )
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        operation_description="특정 게시글을 삭제합니다.",
        responses={
            204: openapi.Response(description="삭제 성공"),
            404: openapi.Response(description="게시글을 찾을 수 없습니다."),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        board_id = self.kwargs.get('board_id')
        post_id = self.kwargs.get('pk')

        try:
            return Post.objects.get(board_id=board_id, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post not found.")

