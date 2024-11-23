from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from ..models.place import Place
from ..models.profile import Profile
from ..models.review import Review
from ..models.rating import Rating
from ..serializers.place import PlaceSerializer
from ..serializers.review import ReviewSerializer
from ..serializers.rating import RatingSerializer  # RatingSerializer 추가
from ..services import NaverMapService


class NearbyCafeListView(ListCreateAPIView):
    """
    현재 위치를 기반으로 1km 이내의 카페를 검색하여 필터링된 리스트 반환.
    """
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        user_lat = profile.latitude
        user_lon = profile.longitude

        # 거리 계산 로직 추가
        cafes = Place.objects.annotate(
            distance=(
                6371 * ACos(
                    Cos(Radians('latitude')) * Cos(Radians(user_lat)) *
                    Cos(Radians('longitude') - Radians(user_lon)) +
                    Sin(Radians('latitude')) * Sin(Radians(user_lat))
                )
            )
        ).filter(distance__lte=1.0)  # 1km 이내 필터링

        return cafes[:5]  # 최대 5개 반환


class CafeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 상세 정보 제공.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_rating(request, cafe_id):
    """
    특정 카페에 별점 추가.
    """
    try:
        cafe = Place.objects.get(id=cafe_id)
        rating_value = request.data.get('rating')

        if not (1 <= int(rating_value) <= 5):
            return Response({"error": "별점은 1에서 5 사이여야 합니다."}, status=400)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            place=cafe,
            defaults={'rating': rating_value}
        )

        # 평균 별점 업데이트
        all_ratings = Rating.objects.filter(place=cafe)
        avg_rating = sum([int(r.rating) for r in all_ratings]) / all_ratings.count()
        cafe.rating = avg_rating
        cafe.save()

        # 직렬화기 사용
        serializer = RatingSerializer(rating)

        return Response({
            "message": "별점이 성공적으로 추가되었습니다.",
            "rating": serializer.data,  # 새로 추가된 별점 데이터 반환
            "average_rating": avg_rating
        }, status=201)

    except Place.DoesNotExist:
        return Response({"error": "해당 카페를 찾을 수 없습니다."}, status=404)


class RatingListView(ListAPIView):
    """
    특정 장소의 별점 목록 반환.
    """
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        cafe_id = self.kwargs.get('cafe_id')
        return Rating.objects.filter(place_id=cafe_id)


class ReviewListCreateView(ListCreateAPIView):
    """
    특정 카페의 리뷰 조회 및 작성.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        cafe_id = self.kwargs['cafe_id']
        return Review.objects.filter(place_id=cafe_id)

    def perform_create(self, serializer):
        cafe = Place.objects.get(id=self.kwargs['cafe_id'])
        serializer.save(user=self.request.user, place=cafe)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 리뷰 수정 및 삭제 (작성자만 가능).
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionError("리뷰를 수정할 권한이 없습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionError("리뷰를 삭제할 권한이 없습니다.")
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def find_meeting_place(request):
    """
    두 사용자의 좌표를 받아 중간 지점 근처 지하철역 검색 및 네이버 길찾기 URL 반환
    """
    try:
        data = request.data
        user1_lat = float(data.get("user1_latitude"))
        user1_lon = float(data.get("user1_longitude"))
        user2_lat = float(data.get("user2_latitude"))
        user2_lon = float(data.get("user2_longitude"))

        cafe_id_user1 = int(data.get("cafe_id_user1"))
        cafe_id_user2 = int(data.get("cafe_id_user2"))

        naver_service = NaverMapService(client_id="your_client_id", client_secret="your_client_secret")

        cafe_user1 = Place.objects.get(id=cafe_id_user1)
        user1_to_cafe_url = naver_service.get_directions_for_user_and_place(user1_lat, user1_lon, cafe_user1.latitude, cafe_user1.longitude)

        cafe_user2 = Place.objects.get(id=cafe_id_user2)
        user2_to_cafe_url = naver_service.get_directions_for_user_and_place(user2_lat, user2_lon, cafe_user2.latitude, cafe_user2.longitude)

        return Response({
            "user1_to_cafe_url": user1_to_cafe_url,
            "user2_to_cafe_url": user2_to_cafe_url,
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def find_single_user_directions(request):
    """
    한 명의 사용자가 자신의 위치에서 선택한 카페로 길찾기 URL 반환
    """
    try:
        data = request.data
        user_lat = float(data.get("user_latitude"))
        user_lon = float(data.get("user_longitude"))

        cafe_id = int(data.get("cafe_id"))

        naver_service = NaverMapService(client_id="your_client_id", client_secret="your_client_secret")

        cafe = Place.objects.get(id=cafe_id)
        directions_url = naver_service.get_directions_for_user_and_place(user_lat, user_lon, cafe.latitude, cafe.longitude)

        return Response({
            "directions_url": directions_url,
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
