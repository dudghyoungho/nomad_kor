from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from ..models.place import Place
from ..models.profile import Profile
from ..models.review import Review
from ..models.rating import Rating
from ..serializers.place import PlaceSerializer
from ..serializers.review import ReviewSerializer


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

        # 프로퍼티 필터링: "집중하기 좋아요" 상위 3위에 포함
        filtered_cafes = [
            cafe for cafe in cafes
            if "집중하기 좋아요" in sorted(cafe.reviews.items(), key=lambda x: x[1], reverse=True)[:3]
        ]

        return filtered_cafes[:5]  # 최대 5개 반환


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

        return Response({
            "message": "별점이 성공적으로 추가되었습니다.",
            "average_rating": avg_rating
        }, status=201)

    except Place.DoesNotExist:
        return Response({"error": "해당 카페를 찾을 수 없습니다."}, status=404)


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
