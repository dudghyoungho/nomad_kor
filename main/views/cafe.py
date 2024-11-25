from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.cafe import Cafe
from ..models.profile import Profile
from ..serializers.cafe import CafeSerializer
from ..services import NaverMapService


# 주변 카페 목록 조회
class NearbyCafeListView(ListCreateAPIView):
    """
    현재 위치를 기반으로 1km 이내의 카페를 검색하여 필터링된 리스트 반환.
    """
    serializer_class = CafeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="주변 카페 목록 조회",
        operation_description="사용자의 현재 위치를 기반으로 1km 이내의 카페를 반환합니다.",
        responses={200: CafeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise ValidationError({"profile": "사용자의 프로필이 존재하지 않습니다."})

        user_lat = profile.latitude
        user_lon = profile.longitude

        cafes = Place.objects.annotate(
            distance=(
                6371 * ACos(
                    Cos(Radians('latitude')) * Cos(Radians(user_lat)) *
                    Cos(Radians('longitude') - Radians(user_lon)) +
                    Sin(Radians('latitude')) * Sin(Radians(user_lat))
                )
            )
        ).filter(distance__lte=1.0)

        return cafes[:5]


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
        operation_description="특정 카페의 상세 정보를 조회합니다.",
        responses={200: CafeSerializer(), 404: "카페를 찾을 수 없습니다."}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


