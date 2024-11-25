from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserDetailsSerializer, UserInfoSerializer
from utils.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from financial_products.models import Deposit, Saving


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

@api_view(['GET'])
def user_list(request):
    users = get_list_or_404(get_user_model())
    serializer = UserInfoSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_product(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    
    if request.user != user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    product_type = request.data.get('product_type')
    product_code = request.data.get('fin_prdt_cd')
    
    if not product_type or product_type not in ['deposit', 'saving']:
        return Response({'error': '잘못된 상품 유형입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if product_type == 'deposit':
            product = get_object_or_404(Deposit, fin_prdt_cd=product_code)
            if user.joined_deposits.filter(fin_prdt_cd=product_code).exists():
                return Response({'error': '이미 가입한 상품입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            user.joined_deposits.add(product)
        else:
            product = get_object_or_404(Saving, fin_prdt_cd=product_code)
            if user.joined_savings.filter(fin_prdt_cd=product_code).exists():
                return Response({'error': '이미 가입한 상품입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            user.joined_savings.add(product)
        
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        print(f"Error in join_product: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_product(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    
    if request.user != user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    product_type = request.data.get('product_type')
    product_code = request.data.get('fin_prdt_cd')
    
    if not product_type or product_type not in ['deposit', 'saving']:
        return Response({'error': '잘못된 상품 유형입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if product_type == 'deposit':
            product = get_object_or_404(Deposit, fin_prdt_cd=product_code)
            user.joined_deposits.remove(product)
        else:
            product = get_object_or_404(Saving, fin_prdt_cd=product_code)
            user.joined_savings.remove(product)
        
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    except Exception as e:
        print(f"Error in cancel_product: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
