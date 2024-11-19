from django.urls import path
from . import views


urlpatterns = [
    path('load_api_data/', views.load_api_data),
    path('deposit_list/', views.deposit_list),
    # path('deposit_option_list/', views.deposit_option_list),
    path('saving_list/', views.saving_list),
]
