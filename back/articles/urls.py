from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('<int:article_pk>/comments/', views.comment_create),
    path('<int:article_pk>/likes/', views.article_likes),
    path('<int:article_pk>/bookmarks/', views.article_bookmarks),
    path('search/', views.article_search),
]
