from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.place import Place
from ..models.profile import Profile
from ..models.review import Review
from ..models.rating import Rating
from ..serializers.place import PlaceSerializer
from ..serializers.review import ReviewSerializer
from ..serializers.rating import RatingSerializer
from ..services import NaverMapService


class NearbyCafeListView(ListCreateAPIView):
    """
    현재 위치를 기반으로 1km 이내의 카페를 검색하여 필터링된 리스트 반환.
    """
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="주변 카페 목록 조회",
        operation_description="사용자의 현재 위치를 기반으로 1km 이내의 카페를 반환합니다.",
        responses={200: PlaceSerializer(many=True)}
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


class CafeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 상세 정보 제공.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="카페 상세 정보 조회",
        operation_description="특정 카페의 상세 정보를 조회합니다.",
        responses={200: PlaceSerializer(), 404: "카페를 찾을 수 없습니다."}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(
    method='post',
    operation_summary="별점 추가",
    operation_description="특정 카페에 별점을 추가합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='별점 (1~5)')},
        required=['rating']
    ),
    responses={
        201: "별점이 성공적으로 추가되었습니다.",
        400: "별점은 1에서 5 사이여야 합니다.",
        404: "카페를 찾을 수 없습니다."
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_rating(request, cafe_id):
    try:
        cafe = Place.objects.get(id=cafe_id)
    except Place.DoesNotExist:
        return Response({"error": "해당 카페를 찾을 수 없습니다."}, status=404)

    rating_value = request.data.get('rating')

    if not rating_value:
        return Response({"error": "별점 값이 누락되었습니다."}, status=400)

    if not (1 <= int(rating_value) <= 5):
        return Response({"error": "별점은 1에서 5 사이여야 합니다."}, status=400)

    rating, created = Rating.objects.update_or_create(
        user=request.user,
        place=cafe,
        defaults={'rating': rating_value}
    )

    all_ratings = Rating.objects.filter(place=cafe)
    avg_rating = sum([int(r.rating) for r in all_ratings]) / all_ratings.count()
    cafe.rating = avg_rating
    cafe.save()

    serializer = RatingSerializer(rating)
    return Response({
        "message": "별점이 성공적으로 추가되었습니다.",
        "rating": serializer.data,
        "average_rating": avg_rating
    }, status=201)


class RatingListView(ListAPIView):
    """
    특정 장소의 별점 목록 반환.
    """
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="별점 목록 조회",
        operation_description="특정 카페의 별점 목록을 반환합니다.",
        responses={200: RatingSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        cafe_id = self.kwargs.get('cafe_id')
        return Rating.objects.filter(place_id=cafe_id)


class ReviewListCreateView(ListCreateAPIView):
    """
    특정 카페의 리뷰 조회 및 작성.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="리뷰 조회 및 작성",
        operation_description="특정 카페의 리뷰를 조회하거나 새로운 리뷰를 작성합니다.",
        responses={200: ReviewSerializer(many=True), 201: ReviewSerializer()},
        request_body=ReviewSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        cafe_id = self.kwargs.get('cafe_id')
        return Review.objects.filter(place_id=cafe_id)

    def perform_create(self, serializer):
        try:
            cafe = Place.objects.get(id=self.kwargs.get('cafe_id'))
        except Place.DoesNotExist:
            raise ValidationError({"cafe": "해당 카페를 찾을 수 없습니다."})
        serializer.save(user=self.request.user, place=cafe)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 리뷰 수정 및 삭제 (작성자만 가능).
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="리뷰 상세 조회, 수정 및 삭제",
        operation_description="특정 리뷰를 조회, 수정하거나 삭제합니다.",
        responses={200: ReviewSerializer(), 204: "삭제 성공", 404: "리뷰를 찾을 수 없습니다."}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

