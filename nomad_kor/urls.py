"""
URL configuration for nomad_kor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main import views
from main.views import signup_view,LoginView
from main.views.comment import CommentListView, CommentDetailView
from main.views.place import add_rating, NearbyCafeListView, CafeDetailView, ReviewListCreateView, ReviewDetailView, \
    find_meeting_place, find_single_user_directions
from main.views.post import PostListView, PostDetailView
from main.views.profile import create_profile,ProfileDetailView, ProfileUpdateView

urlpatterns = [
    # JWT 토큰 발급 (로그인)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # JWT 토큰 갱신
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signup_view, name='signup'),  # 회원가입
    path('login/', LoginView.as_view(), name='login'),  # 로그인
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('places/nearby/', NearbyCafeListView.as_view(), name='nearby_cafes'),  # 근처 카페 리스트
    path('place/detail/<int:pk>/', CafeDetailView.as_view(), name='cafe_detail'),  # 특정 카페 세부 정보
    path('place/<int:cafe_id>/rating/', add_rating, name='add_rating'),  # 별점 추가
    path('place/<int:cafe_id>/reviews/', ReviewListCreateView.as_view(), name='review_list_create'),  # 리뷰 조회 및 작성
    path('place/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),  # 리뷰 수정 및 삭제
    # board_type을 URL 경로로 받아서 처리
    path('boards/<str:board_type>/', views.get_board,name='get_board'),
    path('boards/<int:board_id>/posts/', PostListView.as_view(), name='post_list'),
    path('boards/<int:board_id>/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # 댓글 작성 및 조회
    path('api/boards/<int:board_id>/posts/<int:post_id>/comment/', CommentListView.as_view(), name='comment_list'),
    # 댓글 수정, 삭제 및 조회
    path('api/boards/<int:board_id>/posts/<int:post_id>/comment/<int:pk>/', CommentDetailView.as_view(),
         name='comment_detail'),
    # 두 명의 사용자가 선택한 카페로 길찾기
    path('api/meeting/directions/', find_meeting_place, name='find_meeting_place'),
    # 한 명의 사용자가 선택한 카페로 길찾기
    path('api/user/directions/', find_single_user_directions, name='find_single_user_directions'),
]
# MEDIA_URL과 MEDIA_ROOT 매핑
if settings.DEBUG:  # 디버그 모드에서만 동작하도록
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)