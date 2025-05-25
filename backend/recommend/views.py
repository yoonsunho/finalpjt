# recommend/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
from .utils.recommend import recommend_products
from finlife.serializers import DepositRecommendSerializer, SavingRecommendSerializer

# recommend/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    recommendations = recommend_products(user)
    
    deposit_data = DepositRecommendSerializer(
        recommendations['deposits'], 
        many=True, 
        context={'request': request, 'user': user}
    ).data
    
    saving_data = SavingRecommendSerializer(  # ← 추가된 부분
        recommendations['savings'], 
        many=True, 
        context={'request': request, 'user': user}
    ).data

    return Response({
        'deposits': deposit_data,
        'savings': saving_data
    })
