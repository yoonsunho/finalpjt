from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
import json
from rest_framework import status

from .serializers import UserProfileSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash    # 비밀번호 변경 후 사용자의 세션을 유지(로그아웃 방지)

from rest_framework.response import Response

# Permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# 소셜 로그인
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


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

# 마이페이지 조회 , 수정
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
   user = request.user

    # 조회
   if request.method == 'GET':
       serializer = UserProfileSerializer(user)
       return Response(serializer.data, status = status.HTTP_200_OK)
   
   # 수정
   elif request.method =='PUT':
       serializer = UserProfileUpdateSerializer(
           user, 
           data = request.data, 
           partial = True, 
           context={'request': request})  # context 추가)
       if serializer.is_valid(raise_exception = True):
           serializer.save()
           return Response(serializer.data, status = status.HTTP_200_OK)
           
# 비밀번호 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)  # 세션 유지
        return Response({"detail": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
    

