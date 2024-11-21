import requests

class NaverMapService:
    """
    네이버 지도 API를 호출하여 장소 정보를 검색하는 서비스 클래스.
    """
    BASE_URL = "https://naveropenapi.apigw.ntruss.com/map-place/v1/search"

    def __init__(self, client_id, client_secret):
        """
        네이버 API 호출에 필요한 헤더 설정.
        :param client_id: 네이버 API 클라이언트 ID
        :param client_secret: 네이버 API 클라이언트 Secret
        """
        self.headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }

    def search_place(self, query, latitude=None, longitude=None, radius=None, count=None):
        """
        네이버 지도에서 장소 검색.
        :param query: 검색어 (필수)
        :param latitude: 검색 중심 위도 (선택)
        :param longitude: 검색 중심 경도 (선택)
        :param radius: 검색 반경 (미터, 선택)
        :param count: 최대 결과 개수 (선택)
        :return: 검색된 장소 정보 리스트 (name, address, latitude, longitude 포함)
        """
        if not query:
            raise ValueError("검색어(query)는 필수 입력값입니다.")

        # 요청 파라미터 구성
        params = {
            "query": query,
            "coordinate": f"{longitude},{latitude}" if latitude and longitude else None,
            "radius": radius,  # 검색 반경 (옵션)
            "count": count  # 최대 반환 결과 수 (옵션)
        }

        # API 요청
        response = requests.get(self.BASE_URL, headers=self.headers, params=params)

        # 응답 처리
        if response.status_code == 200:
            data = response.json()
            return self._parse_places(data)
        else:
            response.raise_for_status()

    def _parse_places(self, data):
        """
        API 응답 데이터를 파싱하여 필요한 장소 정보만 추출.
        :param data: 네이버 API 응답 데이터
        :return: 장소 정보 리스트
        """
        places = [
            {
                "name": place.get("name"),
                "address": place.get("road_address"),
                "latitude": float(place.get("y", 0)),
                "longitude": float(place.get("x", 0))
            }
            for place in data.get("places", [])
        ]
        return places

    def calculate_midpoint(self, lat1, lon1, lat2, lon2):
        """
        두 지점 간의 중간 지점 계산
        """
        mid_lat = (lat1 + lat2) / 2
        mid_lon = (lon1 + lon2) / 2
        return mid_lat, mid_lon

    def get_directions_url(self, start_lat, start_lon, goal_lat, goal_lon):
        """
        네이버 지도 길찾기 URL 생성 함수
        """
        return (
            f"https://m.map.naver.com/search2/directions?"
            f"start={start_lat},{start_lon}&goal={goal_lat},{goal_lon}&callback=none"
        )

    def find_nearest_subway_station(self, latitude, longitude):
        """
        중간 지점 또는 사용자의 위치에서 근처 지하철역 검색
        """
        subway_stations = self.search_place("지하철역", latitude, longitude, radius=1000, count=1)
        return subway_stations[0] if subway_stations else None

    def get_directions_for_user_and_place(self, user_lat, user_lon, place_lat, place_lon):
        """
        사용자 위치와 선택한 카페 간의 길찾기 URL 생성
        """
        return self.get_directions_url(user_lat, user_lon, place_lat, place_lon)