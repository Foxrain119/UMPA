from django.urls import path
from . import views

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('users/<username>/', views.profile, name='profile'),
    # path('user_info/', views.user_info, name='user-info'),
] 