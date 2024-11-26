from django.db import models
from django.conf import settings

# 예금
class Deposit(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    fin_prdt_nm = models.TextField()             # 금융 상품명
    fin_co_no = models.TextField()               # 금융회사 코드
    kor_co_nm = models.TextField()               # 금융회사 명
    etc_note = models.TextField()                # 금융 상품 설명
    join_deny = models.IntegerField()            # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()             # 가입 대상
    join_way = models.TextField()                # 가입 방법
    spcl_cnd = models.TextField()                # 우대 조건
    max_limit	= models.IntegerField(null=True)   # 최고한도
    joined_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_deposits', blank=True)
    bookmark_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='book_deposits')


class DepositOption(models.Model):
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, related_name='option')
    intr_rate_type_nm = models.CharField(max_length=2)  # 저축 금리 유형명
    intr_rate = models.FloatField(null=True)            # 저축 금리
    intr_rate2 = models.FloatField(null=True)           # 최고 우대금리
    save_trm = models.IntegerField()                    # 저축 기간 (단위: 개월)


# 적금
class Saving(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    fin_prdt_nm = models.TextField()             # 금융 상품명
    fin_co_no = models.TextField()               # 금융회사 코드
    kor_co_nm = models.TextField()               # 금융회사 명
    etc_note = models.TextField()                # 금융 상품 설명
    join_deny = models.IntegerField()            # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()             # 가입 대상
    join_way = models.TextField()                # 가입 방법
    spcl_cnd = models.TextField()                # 우대 조건
    max_limit	= models.IntegerField(null=True)   # 최고한도
    joined_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_savings', blank=True)
    bookmark_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='book_savings')

  
class SavingOption(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name='option')
    intr_rate_type_nm = models.CharField(max_length=2)  # 저축금리 유형명
    rsrv_type_nm = models.CharField(max_length=10)      # 적립 유형명
    intr_rate = models.FloatField(null=True)            # 저축 금리
    intr_rate2 = models.FloatField(null=True)           # 최고 우대금리
    save_trm = models.IntegerField()                    # 저축 기간 (단위: 개월)
