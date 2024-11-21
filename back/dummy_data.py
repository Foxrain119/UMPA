import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model

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
users = []

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
    gender = random.choice(['M', 'F', 'N'])
    age = random.randint(18, 85)
    marital_status = random.choice([True, False])

    # User 객체 생성
    user = User(
        email=email,
        username=fake.unique.user_name(),
        phone=phone,
        nickname=nickname,
        password=DEFAULT_PASSWORD,
        gender=gender,
        age=age,
        marital_status=marital_status,
        property=random.randint(0, 1_000_000_000)
    )
    users.append(user)

# Bulk Create로 데이터베이스에 삽입
User.objects.bulk_create(users)
print("10,000개의 더미 유저 데이터 생성 완료!")
