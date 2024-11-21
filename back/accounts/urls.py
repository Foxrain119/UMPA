from django.urls import path
from . import views

urlpatterns = [
    path('<username>/', views.profile, name='profile'),
    path('dummy_data/', views.create_dummy_user),
] 