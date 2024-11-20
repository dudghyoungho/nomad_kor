from django.utils.decorators import method_decorator
from django.views import View
from ..models.profile import Profile
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                # JWT 토큰 생성
                refresh = RefreshToken.for_user(user)

                # 프로필 존재 여부 확인
                profile_exists = Profile.objects.filter(user=user).exists()

                return JsonResponse({
                    'message': '로그인 성공!',
                    'username': user.username,
                    'profile_required': not profile_exists,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({'error': '로그인 실패. 아이디 또는 비밀번호를 확인하세요.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f'오류가 발생했습니다: {str(e)}'}, status=500)
