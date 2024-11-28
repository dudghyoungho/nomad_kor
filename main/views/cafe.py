from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import F, FloatField, ExpressionWrapper
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from drf_yasg import openapi
from ..models.cafe import Cafe
from ..models.profile import Profile
from ..serializers.cafe import CafeSerializer
from ..services import NaverMapService

from django.shortcuts import render


# 주변 카페 목록 조회
class NearbyCafeListView(APIView):
    """
    현재 위치를 기반으로 가장 직선거리가 가까운 카페 반환.
    1인 사용자가 주변 카페를 검색 (초기화면) 할 경우 발생
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="1km 이내 카페 목록",
        operation_description="사용자의 현재 위치를 기반으로 1km 이내의 카페 목록을 반환합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 위도"),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 경도"),
            },
            required=['latitude', 'longitude']
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'distance': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        )}
    )
    def post(self, request, *args, **kwargs):
        # 요청 본문에서 좌표 가져오기
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not latitude or not longitude:
            raise ValidationError({"error": "latitude와 longitude 값이 필요합니다."})

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise ValidationError({"error": "latitude와 longitude는 숫자여야 합니다."})

        # 거리 계산 및 1km 이내 카페 필터링
        cafes = Cafe.objects.annotate(
            distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(Radians(F("latitude"))) * Cos(Radians(latitude)) *
                    Cos(Radians(F("longitude")) - Radians(longitude)) +
                    Sin(Radians(F("latitude"))) * Sin(Radians(latitude))
                ),
                output_field=FloatField()
            )
        ).filter(distance__lte=1.0).order_by("distance")[:5]  # 1km 이내 상위 5개

        # 직렬화 및 응답 반환
        serializer = CafeSerializer(cafes, many=True)
        return Response(serializer.data)


class MidpointCafeListView(APIView):
    """
    두 사용자의 중간 지점에서 가장 가까운 카페 5개를 반환합니다.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="중간 지점 근처 카페 목록",
        operation_description="두 사용자의 현재 위치를 받아 중간 지점에서 가장 가까운 카페 5개를 반환합니다.",
        manual_parameters=[
            openapi.Parameter('user1_latitude', openapi.IN_QUERY, description="사용자 1 위도", type=openapi.TYPE_NUMBER),
            openapi.Parameter('user1_longitude', openapi.IN_QUERY, description="사용자 1 경도", type=openapi.TYPE_NUMBER),
            openapi.Parameter('user2_latitude', openapi.IN_QUERY, description="사용자 2 위도", type=openapi.TYPE_NUMBER),
            openapi.Parameter('user2_longitude', openapi.IN_QUERY, description="사용자 2 경도", type=openapi.TYPE_NUMBER),
        ],
        responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'address': openapi.Schema(type=openapi.TYPE_STRING),
                    'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'distance': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        )}
    )
    def get(self, request, *args, **kwargs):
        # 사용자 좌표 가져오기
        user1_lat = request.query_params.get("user1_latitude", None)
        user1_lon = request.query_params.get("user1_longitude", None)
        user2_lat = request.query_params.get("user2_latitude", None)
        user2_lon = request.query_params.get("user2_longitude", None)

        # 좌표 유효성 검사
        if not all([user1_lat, user1_lon, user2_lat, user2_lon]):
            raise ValidationError({"error": "모든 좌표 쿼리 파라미터 (user1_latitude, user1_longitude, user2_latitude, user2_longitude)가 필요합니다."})

        try:
            user1_lat = float(user1_lat)
            user1_lon = float(user1_lon)
            user2_lat = float(user2_lat)
            user2_lon = float(user2_lon)
        except ValueError:
            raise ValidationError({"error": "모든 좌표 값은 숫자여야 합니다."})

        # 중간 지점 계산
        mid_lat = (user1_lat + user2_lat) / 2
        mid_lon = (user1_lon + user2_lon) / 2

        # 중간 지점에서 가까운 카페 조회
        cafes = Cafe.objects.annotate(
            distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(Radians(F("latitude"))) * Cos(Radians(mid_lat)) *
                    Cos(Radians(F("longitude")) - Radians(mid_lon)) +
                    Sin(Radians(F("latitude"))) * Sin(Radians(mid_lat))
                ),
                output_field=FloatField()
            )
        ).filter(distance__lte=5.0).order_by("distance")[:5]  # 5km 이내 상위 5개

        # 카페 데이터를 직렬화하여 응답 반환
        serializer = CafeSerializer(cafes, many=True)
        return Response(serializer.data)



# 카페 상세 조회
class NearbyCafeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 상세 정보 제공.
    """
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="카페 상세 정보 조회",
        operation_description="특정 카페의 상세 정보를 조회합니다 (cafe_name으로 조회).",
        responses={200: CafeSerializer(), 404: "카페를 찾을 수 없습니다."}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        cafe_name을 기준으로 객체를 가져옵니다.
        """
        cafe_name = self.kwargs.get("cafe_name")
        if not cafe_name:
            raise NotFound(detail="카페 이름이 제공되지 않았습니다.")

        try:
            return Cafe.objects.get(name=cafe_name)
        except Cafe.DoesNotExist:
            raise NotFound(detail="해당 이름의 카페를 찾을 수 없습니다.")