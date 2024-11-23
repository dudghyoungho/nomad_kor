# views/anonymous.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models.anonymous import Anonymous
from ..serializers.anonymous import AnonymousSerializer

class AnonymousListView(generics.ListCreateAPIView):
    """
    익명 게시판 목록 조회 및 생성
    """
    queryset = Anonymous.objects.all()
    serializer_class = AnonymousSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AnonymousDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    익명 게시판 상세 조회, 수정 및 삭제
    """
    queryset = Anonymous.objects.all()
    serializer_class = AnonymousSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
