import os
import django
import random
from django.contrib.auth import get_user_model


# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')  # your_project를 실제 프로젝트 이름으로 변경
django.setup()


# User 모델 가져오기
User = get_user_model()
from financial_products.models import Deposit, Saving  # 실제 모델 경로로 변경

# 모든 유저 가져오기
all_users = list(User.objects.all())

# 가입할 유저 수 범위 설정
MIN_USERS_PER_PRODUCT = 1
MAX_USERS_PER_PRODUCT = 50

# 예금 상품에 가입한 사용자 추가
for deposit in Deposit.objects.all():
    num_users = random.randint(MIN_USERS_PER_PRODUCT, MAX_USERS_PER_PRODUCT)
    joined_users = random.sample(all_users, num_users)
    deposit.joined_users.add(*joined_users)
    deposit.save()

print("Deposit 상품에 가입한 사용자 정보 추가 완료!")

# 적금 상품에 가입한 사용자 추가
for saving in Saving.objects.all():
    num_users = random.randint(MIN_USERS_PER_PRODUCT, MAX_USERS_PER_PRODUCT)
    joined_users = random.sample(all_users, num_users)
    saving.joined_users.add(*joined_users)
    saving.save()

print("Saving 상품에 가입한 사용자 정보 추가 완료!")

