from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from ..models.cafe import Cafe
from ..models.review import Review
from ..serializers.review import ReviewSerializer


class ReviewListView(ListCreateAPIView):
    """
    특정 카페의 리뷰 조회 및 작성
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
        return Review.objects.filter(cafe_id=cafe_id)

    def perform_create(self, serializer):
        try:
            cafe = Cafe.objects.get(id=self.kwargs.get('cafe_id'))
        except Cafe.DoesNotExist:
            raise ValidationError({"cafe": "해당 카페를 찾을 수 없습니다."})
        serializer.save(user=self.request.user, cafe=cafe)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 리뷰 수정 및 삭제
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
