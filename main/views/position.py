from ..models import Position
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers.position import PositionSerializer

# Swagger 요청 스키마 정의
position_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='게시판 이름'),
    },
    required=['name']
)

# Swagger 응답 스키마 정의
position_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='게시판 ID'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='게시판 이름'),
    }
)

class PositionListView(ListCreateAPIView):
    """
    게시판 목록 조회 및 생성
    """
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시판 목록 조회 및 생성",
        operation_description="모든 게시판의 목록을 조회하거나 새로운 게시판을 생성합니다.",
        request_body=position_create_request_schema,  # POST 요청에 필요한 데이터 정의
        responses={
            200: openapi.Response(description="목록 조회 성공", schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=position_response_schema
            )),
            201: openapi.Response(description="게시판 생성 성공", schema=position_response_schema),
            400: openapi.Response(description="잘못된 요청"),
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PositionDetailView(RetrieveUpdateDestroyAPIView):
    """
    게시판 상세 조회, 수정 및 삭제
    """
    serializer_class = PositionSerializer
    queryset = Position.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="게시판 상세 조회, 수정 및 삭제",
        operation_description="특정 게시판의 정보를 조회, 수정 또는 삭제합니다.",
        request_body=position_create_request_schema,  # PATCH 요청에 필요한 데이터 정의
        responses={
            200: openapi.Response(description="조회 또는 수정 성공", schema=position_response_schema),
            204: openapi.Response(description="삭제 성공"),
            400: openapi.Response(description="잘못된 요청"),
            404: openapi.Response(description="게시판을 찾을 수 없습니다."),
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
