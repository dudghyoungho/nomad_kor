from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import Post, Board, Profile
from ..serializers import PostSerializer


class IsAuthorOrReadOnly(BasePermission):
    """
    게시글 작성자만 수정 및 삭제 가능
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 요청(GET, HEAD, OPTIONS)은 모두 허용
        if request.method in SAFE_METHODS:
            return True

        # 수정 및 삭제 요청은 작성자만 가능
        return obj.author == request.user.profile


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id를 가져옴
        if not board_id:
            return Post.objects.none()  # board_id가 없으면 빈 리스트 반환
        return Post.objects.filter(board_id=board_id)  # board_id에 해당하는 글만 필터링하여 반환

    def perform_create(self, serializer):
        # 로그인한 사용자의 Profile 가져오기
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            raise ValidationError("User profile not found. Please create a profile first.")

        # URL에서 board_id 가져오기
        board_id = self.kwargs.get('board_id')
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise ValidationError("Board not found.")

        # 요청 데이터에서 title과 content 확인
        title = self.request.data.get("title")
        content = self.request.data.get("content")

        # 필수 값 확인
        if not title or not content:
            raise ValidationError("Title and content are required.")

        # Post 객체 생성 및 저장
        serializer.save(
            board=board,  # URL에서 가져온 board를 명시적으로 설정
            author=profile,  # 로그인한 사용자의 Profile 객체를 author로 설정
            title=title,
            content=content
        )


# 게시판별 글 상세 조회, 수정, 삭제
class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]  # 작성자 권한 추가

    def get_object(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id 가져오기
        post_id = self.kwargs.get('pk')  # URL에서 글 ID 가져오기
        try:
            return Post.objects.get(board_id=board_id, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post not found.")
