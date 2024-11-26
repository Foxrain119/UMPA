from django.urls import path
from django.conf.urls.static import static
from final_project import settings
from . import views

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('users/<str:username>/', views.profile, name='profile'),
    path('users/<str:username>/products/join/', views.join_product, name='join-product'),
    path('users/<str:username>/products/cancel/', views.cancel_product, name='cancel-product'),
    path('static/', views.get_statics),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
