from rest_framework import serializers
from .models import User, minzero_validator
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer
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
        unique_fields = ['phone', 'username']  # 검사할 필드 추가
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
        model = UserModel
        fields = ('pk', 'username', 'email', 'phone', 'age')
        read_only_fields = ('email',) # 변경 불가 필드들

    # 유니크 필드 검증(유효성 검증)
    def validate(self, attrs):
        print("Validating attrs:", attrs)  # 디버깅 출력
        user = self.context['request'].user
        print("Current user:", user)  # 현재 사용자 출력
        unique_fields = ['username', 'phone']
        for field in unique_fields:
            value = attrs.get(field)
            print(f"Checking field {field} with value {value}")  # 필드와 값 출력
            if value:
                # 중복 검사 시 현재 사용자를 제외
                if UserModel.objects.exclude(pk=user.pk).filter(**{field: value}).exists():
                    print(f"Duplicate found for field {field} with value {value}")  # 중복 발견 시 출력
                    raise serializers.ValidationError({
                        field: f'이미 등록된 {field}입니다.'
                    })
        return attrs


# 로그인 custom serializer
# 이메일과 비밀번호만 이용하여 로그인
class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(email, password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

    def get_auth_user(self, email, password):
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
