from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.place import Place
from ..services import NaverMapService


@swagger_auto_schema(
    method='post',
    operation_summary="두 사용자 간의 중간 지점 길찾기",
    operation_description="두 사용자의 좌표와 선택한 카페 ID를 기반으로 각각의 길찾기 URL을 반환합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user1_latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 1 위도"),
            'user1_longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 1 경도"),
            'user2_latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 2 위도"),
            'user2_longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 2 경도"),
            'cafe_id_user1': openapi.Schema(type=openapi.TYPE_INTEGER, description="사용자 1 선택 카페 ID"),
            'cafe_id_user2': openapi.Schema(type=openapi.TYPE_INTEGER, description="사용자 2 선택 카페 ID"),
        },
        required=['user1_latitude', 'user1_longitude', 'user2_latitude', 'user2_longitude', 'cafe_id_user1', 'cafe_id_user2']
    ),
    responses={
        200: openapi.Response(
            description="성공",
            examples={"application/json": {"user1_to_cafe_url": "http://example.com", "user2_to_cafe_url": "http://example.com"}}
        ),
        400: "잘못된 요청 데이터",
        500: "서버 오류"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def find_meeting_place(request):
    """
    두 사용자의 좌표를 받아 중간 지점 근처 지하철역 검색 및 네이버 길찾기 URL 반환
    """
    try:
        data = request.data
        user1_lat = float(data.get("user1_latitude"))
        user1_lon = float(data.get("user1_longitude"))
        user2_lat = float(data.get("user2_latitude"))
        user2_lon = float(data.get("user2_longitude"))

        cafe_id_user1 = int(data.get("cafe_id_user1"))
        cafe_id_user2 = int(data.get("cafe_id_user2"))

        naver_service = NaverMapService(client_id="your_client_id", client_secret="your_client_secret")

        cafe_user1 = Place.objects.get(id=cafe_id_user1)
        user1_to_cafe_url = naver_service.get_directions_for_user_and_place(user1_lat, user1_lon, cafe_user1.latitude, cafe_user1.longitude)

        cafe_user2 = Place.objects.get(id=cafe_id_user2)
        user2_to_cafe_url = naver_service.get_directions_for_user_and_place(user2_lat, user2_lon, cafe_user2.latitude, cafe_user2.longitude)

        return Response({
            "user1_to_cafe_url": user1_to_cafe_url,
            "user2_to_cafe_url": user2_to_cafe_url,
        }, status=200)

    except KeyError as e:
        return Response({"error": f"'{e.args[0]}' 필드가 누락되었습니다."}, status=400)
    except Place.DoesNotExist:
        return Response({"error": "선택한 카페를 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@swagger_auto_schema(
    method='post',
    operation_summary="단일 사용자의 길찾기",
    operation_description="사용자의 좌표와 선택한 카페 ID를 기반으로 길찾기 URL을 반환합니다.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 위도"),
            'user_longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자 경도"),
            'cafe_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="선택한 카페 ID"),
        },
        required=['user_latitude', 'user_longitude', 'cafe_id']
    ),
    responses={
        200: openapi.Response(
            description="성공",
            examples={"application/json": {"directions_url": "http://example.com"}}
        ),
        400: "잘못된 요청 데이터",
        500: "서버 오류"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def find_single_user_direction(request):
    """
    한 명의 사용자가 자신의 위치에서 선택한 카페로 길찾기 URL 반환
    """
    try:
        data = request.data
        user_lat = float(data.get("user_latitude"))
        user_lon = float(data.get("user_longitude"))
        cafe_id = int(data.get("cafe_id"))

        naver_service = NaverMapService(client_id="your_client_id", client_secret="your_client_secret")

        cafe = Place.objects.get(id=cafe_id)
        directions_url = naver_service.get_directions_for_user_and_place(user_lat, user_lon, cafe.latitude, cafe.longitude)

        return Response({
            "directions_url": directions_url,
        }, status=200)

    except KeyError as e:
        return Response({"error": f"'{e.args[0]}' 필드가 누락되었습니다."}, status=400)
    except Place.DoesNotExist:
        return Response({"error": "선택한 카페를 찾을 수 없습니다."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
