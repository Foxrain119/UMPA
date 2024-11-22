import os
import django
import random
from faker import Faker

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')  # your_project를 실제 프로젝트 이름으로 변경
django.setup()

# User 모델 가져오기
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.serializers import CustomRegisterSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
# Faker 객체 생성
fake = Faker()

# 중복 방지를 위한 세트
used_emails = set()
used_nicknames = set()
used_phones = set()

DEFAULT_PASSWORD = "Tjdqls119!"

# REST Framework 요청 객체 생성
factory = APIRequestFactory()
request = factory.post('/accounts/signup/')  # 적절한 URL 경로를 설정하세요

from django.contrib.sessions.middleware import SessionMiddleware

# 요청에 세션 추가 함수
def add_session_to_request(request):
    middleware = SessionMiddleware(lambda x: x)
    middleware.process_request(request)
    request.session.save()

# 요청 생성 후 세션 추가
add_session_to_request(request)


# 더미 데이터 생성
for _ in range(10000):
    # 중복되지 않는 이메일 생성
    email = fake.unique.email()
    while email in used_emails:
        email = fake.unique.email()
    used_emails.add(email)

    # 중복되지 않는 닉네임 생성
    nickname = fake.unique.user_name()
    while nickname in used_nicknames:
        nickname = fake.unique.user_name()
    used_nicknames.add(nickname)

    # 중복되지 않는 전화번호 생성
    phone = fake.unique.msisdn()[:11]
    while phone in used_phones or len(phone) != 11:
        phone = fake.unique.msisdn()[:11]
    used_phones.add(phone)

    # 기타 랜덤 필드 생성
    age = random.randint(18, 85)

    property=random.randint(0, 1_000_000_000)

    gender = random.choice(['M', 'F'])

    marital_status = random.choice([False, True])

    # 데이터 생성
    data = {
        'username': fake.unique.user_name(),
        'email': email,
        'password1': DEFAULT_PASSWORD,
        'password2': DEFAULT_PASSWORD,
        'nickname': nickname,
        'phone': phone,
        'age': age,
        'property': property,
        'gender': gender,
        'marital_status': marital_status
    }

    # def save(self, request):
    #     user = super().save(request)
    #     # Django의 HttpRequest 객체로 접근
    #     django_request = request._request
    #     user.nickname = self.validated_data.get('nickname', '')
    #     user.phone = self.validated_data.get('phone', '')
    #     user.age = self.validated_data.get('age', 0)
    #     user.property = self.validated_data.get('property', 0)
    #     user.marital_status = self.validated_data.get('marital_status', False)
    #     user.save()
    #     return user
    
    # CustomRegisterSerializer를 사용하여 유효성 검사 및 저장
    serializer = CustomRegisterSerializer(data=data, context={'request': Request(request)})
    if serializer.is_valid():
        serializer.save(request=request)
    else:
        print(f"Error with data: {serializer.errors}")

print("10,000개의 더미 유저 데이터 생성 완료!")
