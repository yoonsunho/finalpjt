from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
import json
from rest_framework import status

from .serializers import UserProfileSerializer

from rest_framework.response import Response

# Permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated



User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def check_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        exists = User.objects.filter(email=email).exists()
        return JsonResponse({'available': not exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@api_view(['POST'])
def check_nickname(request):
    try:
        data = json.loads(request.body)
        nickname = data.get('nickname')
        exists = User.objects.filter(nickname=nickname).exists()
        return JsonResponse({'available': not exists})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 마이페이지 조회 함수
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
   try:
       # 현재 로그인한 사용자 정보 직렬화
       serializer = UserProfileSerializer(request.user)
       return Response(serializer.data, status = status.HTTP_200_OK)
   except Exception as e:
       # 예외시 에러 메세지 반환
       return Response({'error':str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)