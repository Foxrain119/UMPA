from django.urls import path
from django.conf.urls.static import static
from final_project import settings
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # media 파일 접근 경로
