from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model
User = get_user_model()

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content')


class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content')
    comment_set = CommentDetailSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

    class LikeUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id',)

    like_users = LikeUserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
        # read_only_fields = ('like_users',)


class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('id', 'title')
    article = ArticleTitleSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # 유저 필드 정보를 문자열로 반환
    # user = serializers.PrimaryKeyRelatedField(read_only=True)  # 유저 필드 정보를 id로 반환
    class Meta:
        model = Comment
        fields = '__all__'
        # read_only_fields = ('article', 'user',)
