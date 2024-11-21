from django.urls import path
from . import views


urlpatterns = [
    path('load_api_data/', views.load_api_data),
    path('list/', views.get_list),
]
