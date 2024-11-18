from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from allauth.account.adapter import DefaultAccountAdapter

# Create your models here.
minzero_validator = MinValueValidator(0)
class User(AbstractUser):
    # AbstractUser 기본필드: password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined
    # 전화 번호
    phone_regex = RegexValidator(
        regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
        message='올바르지 않은 전화번호 형식입니다.'
    )
    phone = models.CharField(
        validators = [phone_regex],
        max_length = 11,
        unique = True,  # 동일 번호로 중복 가입 불가
        null=True,
        blank=True
    )
    
    # 나이
    age = models.IntegerField(
        default=0,
        validators=[minzero_validator]
    )

    # # 자산
    # property = models.IntegerField(
    #     default=0,
    #     validators=[MinValueValidator(0)]
    # )
    
    # # 결혼 여부
    # marital_status = models.BooleanField(
    #     default=False
    # )
    
    # # 프로필 이미지
    # profile_img = ProcessedImageField(
    #     blank=True,
    #     upload_to='profile_img/%Y/%m',
    #     processors=[ResizeToFill(300, 300)],
    #     format='JPEG',
    #     options={'quality': 70},
    # )

    # 찜 목록
    # custom_page (list)
    # 가입한 예금 리스트
    # 가입한 적금 리스트
    def __str__(self):
        return self.username


# 어댑터 커스텀
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