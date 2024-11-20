from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from ..models.board import Board
from ..serializers.board import BoardSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])  # 인증된 사용자만 접근 가능, 비인증 사용자는 읽기만 가능
def get_board(request, board_type):
    """
    특정 게시판 목록 반환 (네트워킹/자유 게시판)
    """
    # board_type에 맞는 게시판 필터링
    boards = Board.objects.filter(name=board_type)

    # 게시판이 없다면 빈 리스트 반환 (선택적으로 오류 처리 추가 가능)
    if not boards:
        return Response({"message": "No boards found for this type."}, status=404)

    # 게시판 데이터를 직렬화하여 반환
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)
