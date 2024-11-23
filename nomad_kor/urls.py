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

# main 앱의 views import
from main.views.signup import signup_view  # signup 관련 수정
from main.views.login import LoginView  # Login 관련 수정
from main.views.profile import create_profile, ProfileDetailView, ProfileUpdateView
from main.views.position import PositionListView, PositionDetailView
from main.views.ftf import FTFListView, FTFDetailView
from main.views.anonymous import AnonymousListView, AnonymousDetailView
from main.views.post import PostListView, PostDetailView
from main.views.comment import CommentListView, CommentDetailView
from main.views.place import (
    add_rating, NearbyCafeListView, CafeDetailView,
    ReviewListCreateView, ReviewDetailView, find_meeting_place,
    find_single_user_directions, RatingListView
)

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # JWT 토큰
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 인증 및 프로필
    path('signup/', signup_view, name='signup'),
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
    path('meeting-place/', find_meeting_place, name='find-meeting-place'),
    path('single-directions/', find_single_user_directions, name='single-directions'),

    # Position 게시판
    path('networking/position/', PositionListView.as_view(), name='position-list-create'),
    path('networking/position/<int:position_id>/', PositionDetailView.as_view(), name='position-detail'),
    # Position 게시판의 게시글
    path('networking/position/<int:position_id>/posts/', PostListView.as_view(), name='position-post-list'),
    path('networking/position/<int:position_id>/posts/<int:pk>/', PostDetailView.as_view(), name='position-post-detail'),
    # Position 게시판 댓글
    # 게시글에 대한 댓글을 작성하기 위한 URL
    path('networking/position/<int:position_id>/posts/<int:post_id>/comments/', CommentListView.as_view(),
         name='position-comment-list'),
    path('networking/position/<int:position_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(),
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
