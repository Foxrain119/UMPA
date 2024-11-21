from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.postgres.fields import ArrayField

minzero_validator = MinValueValidator(0)
class User(AbstractUser):
    # phone_regex = RegexValidator(
    #     regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
    #     message='올바르지 않은 전화번호 형식입니다.'
    # )
    # phone = models.CharField(
    #     validators = [phone_regex],
    #     max_length = 11,
    #     unique = True,  # 동일 번호로 중복 가입 불가
    #     null=True,
    #     blank=True
    # )

    # age = models.IntegerField(
    #     default=0,
    #     validators=[minzero_validator]
    # )
    phone = models.CharField(max_length=11, blank=True)

    age = models.IntegerField(null=True, blank=True)
    
    profile_img = ProcessedImageField(
        upload_to='profile_images/',
        processors=[ResizeToFill(200, 200)],  # 이미지 리사이징
        format='JPEG',
        options={'quality': 90},
        blank=True,
        null=True,
        default='default_profile.jpg'  # 기본 이미지 파일명 (static 폴더에 위치)
    )
    
    nickname = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True
    )

    # bookmark_product_list = models.JSONField(
    #     default=list,
    #     blank=True,
    #     null=True
    # )

    bookmark_product_list = ArrayField(models.IntegerField(blank=True))

    # bookmark_article_list = models.JSONField(
    #     default=list,
    #     blank=True,
    #     null=True
    # )

    # bookmark_article_list = ArrayField(models.IntegerField(blank=True))

    # liked_article_list = models.JSONField(
    #     default=list,
    #     blank=True,
    #     null=True
    # )
    liked_article_list = ArrayField(models.IntegerField(blank=True))

    GENDER_CHOICES = [
        ('N', '선택'),
        ('M', '남성'),
        ('F', '여성')
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',
        blank=True
    )
    
    property = models.BigIntegerField(
        verbose_name='자산',
        validators=[MinValueValidator(0)],
        default=0
    )
    
    marital_status = models.BooleanField(
        verbose_name='결혼 여부',
        default=False
    )
    
    # financial_products = models.JSONField(
    #     verbose_name='가입 상품 목록',
    #     default=list,
    #     blank=True,
    #     null=True
    # )
    
    # contracted_deposit = models.JSONField(
    #     verbose_name='가입 예금 목록',
    #     default=list,
    #     blank=True,
    #     null=True
    # )
    contracted_deposit = ArrayField(models.IntegerField(blank=True))
    
    # contracted_savings = models.JSONField(
    #     verbose_name='가입 적금 목록',
    #     default=list,
    #     blank=True,
    #     null=True
    # )
    contracted_savings = ArrayField(models.IntegerField(blank=True))
    # salary = models.BigIntegerField(
    #     verbose_name='연봉',
    #     validators=[MinValueValidator(0)],
    #     default=0
    # )

    # TENDENCY_CHOICES = [
    #     ('NO', '선택'),
    #     ('AG', '공격 투자형'),
    #     ('AC', '적극 투자형'),
    #     ('NE', '위험 중립형'),
    #     ('CO', '안정 추구형'),
    #     ('ST', '안정형')
    # ]
    # tendency = models.CharField(
    #     verbose_name='투자 성향',
    #     max_length=2,
    #     choices=TENDENCY_CHOICES,
    #     default='NO',
    #     blank=True
    # ) 

    def __str__(self):
        return self.username


# 어댑터 커스텀(미완성)
class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # 필드를 추가
        phone = data.get("phone")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if phone:
            user_field(user, "phone", phone)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user