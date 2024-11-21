# views/post.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from ..models import Post, Board, Profile
from ..serializers import PostSerializer


class PostListView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id를 가져옴
        if not board_id:
            return Post.objects.none()  # board_id가 없으면 빈 리스트 반환
        return Post.objects.filter(board_id=board_id)  # board_id에 해당하는 글만 필터링하여 반환

    def perform_create(self, serializer):
        # 요청 본문에서 데이터를 가져옵니다.
        title = self.request.data.get("title")
        content = self.request.data.get("content")

        # 필수 항목이 없으면 오류 처리
        if not title or not content:
            raise ValidationError("Title and content are required.")

        # 로그인한 사용자의 Profile을 가져옵니다.
        profile = self.request.user.profile  # request.user.profile로 로그인한 사용자의 프로필을 가져옵니다.

        # URL에서 board_id 가져오기
        board_id = self.kwargs.get('board_id')

        # 게시판 찾기
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise ValidationError("Board not found.")

        # `Post` 객체 생성
        post = serializer.save(
            board=board,
            author=profile,  # `author`는 로그인한 사용자의 `Profile` 객체로 설정
            title=title,
            content=content
        )
        return post


# 게시판별 글 상세 조회, 수정, 삭제
class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        board_id = self.kwargs.get('board_id')  # URL에서 board_id 가져오기
        post_id = self.kwargs.get('pk')  # URL에서 글 ID 가져오기
        try:
            return Post.objects.get(board_id=board_id, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post not found.")

