from ..models import Position  # 한 단계 상위 디렉토리에서 models 가져오기
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.http import Http404

from ..serializers.position import PositionSerializer  # PositionSerializer 경로도 확인

class PositionListView(ListCreateAPIView):
    """
    게시판 목록 조회 및 생성
    """
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class PositionDetailView(RetrieveUpdateDestroyAPIView):
    """
    게시판 상세 조회, 수정 및 삭제
    """
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
