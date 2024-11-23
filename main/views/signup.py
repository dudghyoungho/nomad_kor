from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])  # JWT 검사를 비활성화하여 누구나 접근 가능
def signup_view(request):
    try:
        # POST 요청 데이터 가져오기
        data = request.data

        username = data.get("username")
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        # 입력 필드 확인
        if not username or not password or not password_confirm:
            return JsonResponse({"error": "모든 필드를 입력해주세요."}, status=400)

        # 중복된 아이디 확인
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "이미 사용 중인 아이디입니다."}, status=400)

        # 비밀번호 일치 확인
        if password != password_confirm:
            return JsonResponse({"error": "비밀번호가 일치하지 않습니다."}, status=400)

        # 사용자 생성
        User.objects.create(
            username=username,
            password=make_password(password)  # 비밀번호 암호화
        )

        return JsonResponse({"message": "회원가입이 완료되었습니다."}, status=201)

    except Exception as e:
        return JsonResponse({"error": f"오류가 발생했습니다: {str(e)}"}, status=500)


