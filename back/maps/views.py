from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests

@api_view(['GET'])
def search_banks(request):
    province = request.GET.get('province')
    district = request.GET.get('district')
    bank = request.GET.get('bank')
    
    # 필수 파라미터 검증
    if not all([province, district]):
        return Response({
            'error': '시/도와 구/군 정보는 필수입니다.'
        }, status=400)
    
    # 검색어 생성
    query = f"{province} {district} {bank}".strip()
    
    # REST API 키 확인
    if not settings.KAKAO_MAP_REST_API_KEY:
        return Response({
            'error': 'Kakao REST API key is not configured'
        }, status=500)
    
    # 카카오맵 API 호출
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_MAP_REST_API_KEY}'
    }
    
    try:
        response = requests.get(
            'https://dapi.kakao.com/v2/local/search/keyword.json',
            headers=headers,
            params={
                'query': query,
                'category_group_code': 'BK9',  # 은행 카테고리
                'size': 15,  # 한 페이지에 보여질 문서 수
                'page': 1,   # 페이지 번호
                'sort': 'distance',  # 거리순 정렬
                'x': '126.977941',  # 경도(longitude)
                'y': '37.566295'    # 위도(latitude)
            }
        )
        
        if response.status_code != 200:
            return Response({
                'error': '카카오맵 API 호출 실패',
                'status': response.status_code,
                'detail': response.text
            }, status=response.status_code)
        
        # 응답 데이터 가공
        data = response.json()
        places = data.get('documents', [])
        meta = data.get('meta', {})
        
        # 검색 결과가 없는 경우
        if not places:
            return Response({
                'places': [],
                'meta': {
                    'total_count': 0,
                    'is_end': True,
                    'message': '검색 결과가 없습니다.'
                }
            })
        
        results = {
            'places': [
                {
                    'id': place['id'],
                    'name': place['place_name'],
                    'address': place['address_name'],
                    'road_address': place['road_address_name'],
                    'lat': float(place['y']),
                    'lng': float(place['x']),
                    'phone': place.get('phone', ''),
                    'place_url': place['place_url'],
                    'distance': place.get('distance', ''),
                    'category_name': place['category_name']
                } for place in places
            ],
            'meta': {
                'total_count': meta.get('total_count', 0),
                'pageable_count': meta.get('pageable_count', 0),
                'is_end': meta.get('is_end', True)
            }
        }
        
        return Response(results)
        
    except requests.exceptions.RequestException as e:
        return Response({
            'error': '서버 오류가 발생했습니다.',
            'detail': str(e)
        }, status=500)
    except Exception as e:
        return Response({
            'error': '서버 오류가 발생했습니다.',
            'detail': str(e)
        }, status=500)

@api_view(['GET'])
def get_locations(request):
    try:
        # 은행 목록 - 카카오맵 API에서 카테고리 검색이 불가능하여 정적 데이터 사용
        banks = [
            {'name': '국민은행'},
            {'name': '신한은행'},
            {'name': '우리은행'},
            {'name': '하나은행'},
            {'name': 'SC제일은행'},
            {'name': '케이뱅크'},
            {'name': '카카오뱅크'},
            {'name': '토스뱅크'},
            {'name': '농협은행'},
            {'name': '기업은행'},
            {'name': '수협은행'},
            {'name': '대구은행'},
            {'name': '부산은행'},
            {'name': '경남은행'},
            {'name': '광주은행'},
            {'name': '전북은행'},
            {'name': '제주은행'}
        ]
        
        # 행정구역 데이터 (정적 데이터)
        locations = {
            '서울특별시': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', 
                        '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', 
                        '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', 
                        '은평구', '종로구', '중구', '중랑구'],
            '부산광역시': ['강서구', '금정구', '남구', '동구', '동래구', '부산진구', '북구', 
                        '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구'],
            '대구광역시': ['남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구'],
            '인천광역시': ['강화군', '계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구'],
            '광주광역시': ['광산구', '남구', '동구', '북구', '서구'],
            '대전광역시': ['대덕구', '동구', '서구', '유성구', '중구'],
            '울산광역시': ['남구', '동구', '북구', '울주군', '중구'],
            '경기도': ['가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', 
                    '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', 
                    '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', 
                    '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시']
        }
        
        return Response({
            'provinces': list(locations.keys()),
            'districts': locations,
            'banks': sorted(banks, key=lambda x: x['name'])  # 은행명 기준 정렬
        })
        
    except Exception as e:
        return Response({
            'error': '서버 오류가 발생했습니다.',
            'detail': str(e)
        }, status=500) 