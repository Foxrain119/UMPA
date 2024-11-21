from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.profile, name='profile'),
    path('user_info/', views.user_info, name='user-info'),
] 