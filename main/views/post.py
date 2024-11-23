from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.http import Http404
from ..serializers.post import PostSerializer
from ..models import Position, FTF, Anonymous, Profile  # FTF 모델을 추가로 임포트

class PostListView(ListCreateAPIView):
    """
    게시글 목록 조회 및 생성
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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

            # 게시글 저장 (Position 게시판)
            serializer.save(position=position, author=self.request.user.profile,
                            author_name=self.request.user.profile.nickname)

        elif 'ftf' in path:
            ftf_id = self.kwargs.get('ftf_id')
            if not ftf_id:
                raise ValidationError({"ftf": "FTF ID is missing from the request URL."})

            try:
                ftf = FTF.objects.get(id=ftf_id)
            except FTF.DoesNotExist:
                raise ValidationError({"ftf": f"FTF with the given ID {ftf_id} does not exist."})

            # 게시글 저장 (FTF 게시판)
            serializer.save(ftf=ftf, author=self.request.user.profile, author_name=self.request.user.profile.nickname)

        elif 'anonymous' in path:
            anonymous_id = self.kwargs.get('anonymous_id')
            if not anonymous_id:
                raise ValidationError({"anonymous": "Anonymous ID is missing from the request URL."})

            try:
                anonymous = Anonymous.objects.get(id=anonymous_id)
            except Anonymous.DoesNotExist:
                raise ValidationError(
                    {"anonymous": f"Anonymous board with the given ID {anonymous_id} does not exist."})

            # 게시글 저장 (익명 게시판)
            serializer.save(anonymous=anonymous, author=self.request.user.profile,
                            author_name="익명")  # 익명 게시판은 "익명"으로 저장

        else:
            raise ValidationError({"error": "Invalid board type in URL."})


class PostDetailView(RetrieveUpdateDestroyAPIView):
    """
    게시글 상세 조회, 수정 및 삭제
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        board_id = self.kwargs.get('board_id')
        post_id = self.kwargs.get('pk')

        try:
            return Post.objects.get(board_id=board_id, id=post_id)
        except Post.DoesNotExist:
            raise Http404("Post not found.")
