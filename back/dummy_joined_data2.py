import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.serializers import CustomRegisterSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')  # your_project를 실제 프로젝트 이름으로 변경
django.setup()

# User 모델 가져오기
User = get_user_model()

# Faker 객체 생성
fake = Faker()

# 중복 방지를 위한 세트
used_emails = set()
used_nicknames = set()
used_phones = set()

DEFAULT_PASSWORD = "password123"

# REST Framework 요청 객체 생성
factory = APIRequestFactory()
request = factory.post('/accounts/signup/')  # 적절한 URL 경로를 설정하세요

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

    # 데이터 생성
    data = {
        'username': fake.unique.user_name(),
        'email': email,
        'password1': DEFAULT_PASSWORD,
        'password2': DEFAULT_PASSWORD,
        'nickname': nickname,
        'phone': phone,
        'age': age,
    }

    # CustomRegisterSerializer를 사용하여 유효성 검사 및 저장
    serializer = CustomRegisterSerializer(data=data, context={'request': Request(request)})
    if serializer.is_valid():
        serializer.save(request=request)
    else:
        print(f"Error with data: {serializer.errors}")

print("10,000개의 더미 유저 데이터 생성 완료!")
