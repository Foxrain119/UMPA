from django.urls import path
from . import views


urlpatterns = [
    path('load_api_data/', views.load_api_data),
    path('deposit_list/', views.deposit_list),
    path('saving_list/', views.saving_list),
    path('products/', views.product_list),
    path('products/<str:product_id>/', views.product_detail),
]
