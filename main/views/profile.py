from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.profile import Profile
from ..serializers.profile import ProfileSerializer

# Swagger 요청 스키마 정의
profile_create_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 닉네임'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='나이'),
        'gender': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="성별 ('M': 남성, 'F': 여성)"
        ),
        'job': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="직군 ('FE': 프론트엔드, 'BE': 백엔드, 'ST': 창업가, 'CT': 크리에이터, 'MK': 마케터)"
        ),
        'area': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='활동 지역 (서울특별시 구 이름, 예: "서울특별시 종로구")'
        ),
    },
    required=['nickname', 'age', 'gender', 'job', 'area']
)

profile_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 닉네임'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='나이'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='성별'),
        'job': openapi.Schema(type=openapi.TYPE_STRING, description='직군'),
        'area': openapi.Schema(type=openapi.TYPE_STRING, description='활동 지역'),
    }
)

profile_error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='오류 메시지'),
    }
)

@swagger_auto_schema(
    method='post',
    operation_summary="프로필 생성",
    operation_description="닉네임, 나이, 성별, 직군, 활동 지역 정보를 입력하여 새로운 프로필을 생성합니다.",
    request_body=profile_create_request_schema,
    responses={
        201: openapi.Response(description="프로필 생성 성공", schema=profile_response_schema),
        400: openapi.Response(description="잘못된 요청", schema=profile_error_schema),
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):
    """
    프로필 생성 (nickname, age, gender, job, area 필수)
    """
    user = request.user
    if Profile.objects.filter(user=user).exists():
        return Response({"error": "프로필이 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    serializer = ProfileSerializer(data=data)
    if serializer.is_valid():
        profile = serializer.save(user=user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(RetrieveAPIView):
    """
    프로필 조회
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="프로필 조회",
        operation_description="현재 로그인된 사용자의 프로필 정보를 반환합니다.",
        responses={
            200: openapi.Response(description="프로필 조회 성공", schema=profile_response_schema),
            404: openapi.Response(description="프로필이 존재하지 않음"),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        현재 로그인된 유저의 프로필 반환
        """
        return Profile.objects.get(user=self.request.user)


class ProfileUpdateView(RetrieveUpdateAPIView):
    """
    프로필 조회 및 업데이트
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="프로필 조회 및 업데이트",
        operation_description="현재 로그인된 사용자의 프로필을 조회하거나 수정합니다.",
        responses={
            200: openapi.Response(description="프로필 조회 또는 업데이트 성공", schema=profile_response_schema),
            400: openapi.Response(description="잘못된 요청", schema=profile_error_schema),
            404: openapi.Response(description="프로필이 존재하지 않음"),
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        현재 로그인된 유저의 프로필 반환
        """
        return Profile.objects.get(user=self.request.user)
