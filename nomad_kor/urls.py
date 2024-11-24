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
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# 인증 및 프로필 관련 뷰
from main.views.signup import SignupView
from main.views.login import LoginView
from main.views.profile import create_profile, ProfileDetailView, ProfileUpdateView

# 게시판 관련 뷰
from main.views.position import PositionListView, PositionDetailView
from main.views.ftf import FTFListView, FTFDetailView
from main.views.anonymous import AnonymousListView, AnonymousDetailView
from main.views.post import PostListView, PostDetailView
from main.views.comment import CommentListView, CommentDetailView

# 카페 및 장소 관련 뷰
from main.views.place import (
    add_rating, NearbyCafeListView, CafeDetailView,
    ReviewListCreateView, ReviewDetailView, RatingListView,
)
#길찾기 관련 뷰
from main.views.direction import find_meeting_place, find_single_user_direction

schema_view = get_schema_view(
    openapi.Info(
        title="Nomad_Kor API",
        default_version='v1',
        description="Nomad_Kor 프로젝트의 API 문서",
        contact=openapi.Contact(email="chsm7288@naver.com"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # JWT 토큰
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger URLs 추가
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # 인증 및 프로필
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    # 카페 관련
    path('places/nearby/', NearbyCafeListView.as_view(), name='nearby-cafes'),
    path('places/<int:cafe_id>/', CafeDetailView.as_view(), name='cafe-detail'),
    path('places/<int:cafe_id>/add-rating/', add_rating, name='add-rating'),
    path('places/<int:cafe_id>/ratings/', RatingListView.as_view(), name='rating-list'),
    path('places/<int:cafe_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # 길찾기
    path('directions/meeting/', find_meeting_place, name='find-meeting-place'),
    path('directions/single/', find_single_user_direction, name='find-single-user-direction'),

    # Position 게시판
    path('network/position/', PositionListView.as_view(), name='position-list'),
    path('network/position/<int:position_id>/', PositionDetailView.as_view(), name='position-detail'),
    # Position 게시판의 게시글
    path('network/position/<int:position_id>/posts/', PostListView.as_view(), name='position-post-list'),
    path('network/position/<int:position_id>/posts/<int:pk>/', PostDetailView.as_view(), name='position-post-detail'),
    # Position 게시판 댓글
    # 게시글에 대한 댓글을 작성하기 위한 URL
    path('network/position/<int:position_id>/posts/<int:post_id>/comments/', CommentListView.as_view(),
         name='position-comment-list'),
    path('network/position/<int:position_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(),
         name='position-comment-detail'),

    # FTF 게시판
    path('network/ftf/', FTFListView.as_view(), name='ftf-list'),
    path('network/ftf/<int:ftf_id>/', FTFDetailView.as_view(), name='ftf-detail'),
    path('network/ftf/<int:ftf_id>/posts/', PostListView.as_view(), name='ftf-post-list'),
    path('network/ftf/<int:ftf_id>/posts/<int:pk>/', PostDetailView.as_view(), name='ftf-post-detail'),
    path('network/ftf/<int:ftf_id>/posts/<int:post_id>/comments/', CommentListView.as_view(), name='ftf-comment-list'),
    path('network/ftf/<int:ftf_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='ftf-comment-detail'),

    # 익명 게시판
    path('network/anonymous/', AnonymousListView.as_view(), name='anonymous-list'),
    path('network/anonymous/<int:anonymous_id>/', AnonymousDetailView.as_view(), name='anonymous-detail'),
    path('network/anonymous/<int:anonymous_id>/posts/', PostListView.as_view(), name='anonymous-post-list'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:pk>/', PostDetailView.as_view(), name='anonymous-post-detail'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:post_id>/comments/', CommentListView.as_view(), name='anonymous-comment-list'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='anonymous-comment-detail'),
]

# 미디어 파일 제공 (개발 환경에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
