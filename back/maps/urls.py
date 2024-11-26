from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_banks, name='search_banks'),
    path('locations/', views.get_locations, name='get_locations'),
] 