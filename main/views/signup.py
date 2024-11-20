from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            password_confirm = data.get("password_confirm")

            if not username or not password or not password_confirm:
                return JsonResponse({"error": "모든 필드를 입력해주세요."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "이미 사용 중인 아이디입니다."}, status=400)

            if password != password_confirm:
                return JsonResponse({"error": "비밀번호가 일치하지 않습니다."}, status=400)

            user = User.objects.create(
                username=username,
                password=make_password(password)
            )
            return JsonResponse({"message": "회원가입이 성공적으로 완료되었습니다!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "유효하지 않은 JSON 데이터입니다."}, status=400)

    return JsonResponse({"error": "POST 요청만 허용됩니다."}, status=405)
