# views/ftf.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models.ftf import FTF
from ..serializers.ftf import FTFSerializer

class FTFListView(generics.ListCreateAPIView):
    """
    FTF 게시판 목록 조회 및 생성
    """
    queryset = FTF.objects.all()
    serializer_class = FTFSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FTFDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    FTF 게시판 상세 조회, 수정 및 삭제
    """
    queryset = FTF.objects.all()
    serializer_class = FTFSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
