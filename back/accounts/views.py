from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserDetailsSerializer
from utils.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == 'GET':
        serializer = CustomUserDetailsSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': '회원탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
