from rest_framework import serializers
from .models import User, minzero_validator
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# 회원 가입 custom serializer
class CustomRegisterSerializer(RegisterSerializer):
    # 필드 추가
    phone = serializers.CharField(
        max_length = 11,
        validators=[User.phone_regex],
        required=False
    )
    age = serializers.IntegerField(
        required=True,
        validators=[minzero_validator]
    )

    # 동적으로 unique 속성 필드에 대한 중복 검사
    def validate(self, attrs):
        unique_fields = ['phone', ]  # 검사할 필드 추가
        for field in unique_fields:
            value = attrs.get(field)
            if value and User.objects.filter(**{field: value}).exists():
                raise serializers.ValidationError({field: f"이미 등록된 {field} 입니다."})
        return attrs

    # 추가한 필드 저장
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            # 추가 필드 작성
            'phone': self.validated_data.get('phone', ''),
            'age': self.validated_data.get('age', 0),
        }
    
    # 추가 로직(로그 기록, 외부 API 호출 등) 구현 시 필요한 save 메서드 오버라이드
    def save(self, request):
        user = super().save(request)
        # 추가 필드
        user.phone = self.validated_data.get('phone', '')
        user.age = self.validated_data.get('age', 0)
        user.save()
        return user



# 회원 정보 custom serializer
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'phone'):
            extra_fields.append('phone')
        if hasattr(UserModel, 'age'):
            extra_fields.append('age')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)