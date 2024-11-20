from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from ..models import Post, Board, Profile
from ..serializers import PostSerializer


class IsPostAuthorPermission(BasePermission):
    """
    글 작성자만 수정 및 삭제 가능.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author.user == request.user  # 작성자만 수정/삭제 가능
        return True


# 게시판별 글 목록 조회 및 생성
from rest_framework.exceptions import ValidationError


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id를 가져옴
        if not board_id:
            return Post.objects.none()  # board_id가 없으면 빈 리스트 반환
        return Post.objects.filter(board_id=board_id)  # board_id에 해당하는 글만 필터링하여 반환

    def perform_create(self, serializer):
        board_id = self.request.data.get("board_id")
        title = self.request.data.get("title")
        content = self.request.data.get("content")
        nickname = self.request.data.get("nickname")  # nickname을 받아옴

        if not board_id or not title or not content or not nickname:
            raise ValidationError("Board ID, title, content, and nickname are required.")

        # nickname으로 Profile을 찾음
        try:
            profile = Profile.objects.get(nickname=nickname)  # nickname으로 Profile을 검색
        except Profile.DoesNotExist:
            raise ValidationError(f"Profile with nickname '{nickname}' does not exist.")

        board = Board.objects.get(id=board_id)

        # `author` 필드를 `nickname`으로 찾은 `Profile`로 설정
        serializer.save(
            board=board,
            author=profile,  # Profile 객체를 `author`로 설정
            title=title,
            content=content
        )


# 게시판별 글 상세 조회, 수정, 삭제
class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthorPermission]

    def get_object(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id 가져오기
        post_id = self.kwargs.get('pk')  # URL에서 글 ID 가져오기
        try:
            return Post.objects.get(board_id=board_id, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post not found.")

