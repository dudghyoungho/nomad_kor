from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# Swagger 요청 스키마 정의
signup_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='사용자 아이디'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호'),
        'password_confirm': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호 확인'),
    },
    required=['username', 'password', 'password_confirm']
)

# Swagger 응답 정의
signup_success_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='성공 메시지'),
    }
)

signup_error_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(type=openapi.TYPE_STRING, description='오류 메시지'),
    }
)

class SignupView(APIView):
    permission_classes = []  # 인증 없이 접근 가능

    @swagger_auto_schema(
        operation_summary="회원가입",
        operation_description="새로운 사용자를 생성합니다.",
        request_body=signup_request_schema,  # 요청 본문 데이터 정의
        responses={
            201: openapi.Response(description="회원가입 성공", schema=signup_success_response),
            400: openapi.Response(description="잘못된 요청", schema=signup_error_response),
            500: openapi.Response(description="서버 오류", schema=signup_error_response),
        }
    )
    def post(self, request):
        """
        회원가입 API
        사용자 아이디, 비밀번호, 비밀번호 확인을 입력받아 새 사용자를 생성합니다.
        """
        data = request.data
        username = data.get("username")
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        # 입력 필드 확인
        if not username or not password or not password_confirm:
            return Response({"error": "모든 필드를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 중복된 아이디 확인
        if User.objects.filter(username=username).exists():
            return Response({"error": "이미 사용 중인 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 일치 확인
        if password != password_confirm:
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성
        try:
            User.objects.create(
                username=username,
                password=make_password(password)  # 비밀번호 암호화
            )
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



