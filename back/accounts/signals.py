# 인증된 사용자가 회원가입에 성공하면 자동으로 해당 사용자에게 토큰을 응답하는 코드
# DRF 공식문서 참고 (Django Signals; 이벤트 알림 시스템)
# 애플리케이션 내에서 특정 이벤트가 발생할 때, 다른 부분에게 신호를 보내어 이벤트가 발생했음을 알릴 수 있음
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
