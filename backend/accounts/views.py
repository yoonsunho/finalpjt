from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login
from django.conf import settings # 추가
from django.db import IntegrityError
from rest_framework.decorators import api_view
import json
import requests
import random
from rest_framework import status


from .serializers import UserProfileSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash    # 비밀번호 변경 후 사용자의 세션을 유지(로그아웃 방지)

from rest_framework.response import Response

# Permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

# 소셜 로그인
from rest_framework.authtoken.models import Token

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
    

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    구글 소셜 로그인 핸들러
    1. 구글 인증 코드 검증
    2. 임시 사용자 생성 (프로필 미완료 상태)
    3. 추가 정보 입력 필요 응답
    """
    # 1. 프론트엔드에서 전달한 인증 코드 추출
    code = request.data.get('code')
    redirect_uri = request.data.get('redirect_uri')
    
    # 필수 파라미터 검증
    if not code or not redirect_uri:
        return Response(
            {'error': 'code와 redirect_uri는 필수입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. 구글 OAuth2 토큰 엔드포인트 요청
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    
    try:
        # 3. 인증 코드를 액세스 토큰으로 교환
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        access_token = token_response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': '구글 토큰 요청 실패', 'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4. 액세스 토큰으로 사용자 정보 조회
    userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
        email = userinfo.get('email')
        
        if not email:
            return Response(
                {'error': '이메일 정보를 가져올 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': '사용자 정보 요청 실패', 'detail': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. 기존 사용자 확인
    try:
        user = User.objects.get(email=email)
        # 기존 사용자: 바로 로그인 처리
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'key': token.key})
    except User.DoesNotExist:
        # 6. 신규 사용자: 임시 계정 생성
        base_nickname = email.split('@')[0][:15]  # 이메일 앞부분 15자리 사용
        temp_nickname = None
        
        # 중복되지 않는 닉네임 생성 (최대 5회 시도)
        for _ in range(5):
            suffix = str(random.randint(1000, 9999))
            temp_nickname = f"{base_nickname}_{suffix}"
            if not User.objects.filter(nickname=temp_nickname).exists():
                break
        else:
            return Response(
                {'error': '임시 닉네임 생성 실패'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 7. 임시 사용자 생성 (프로필 미완료 상태)
        try:
            user = User.objects.create(
                email=email,
                nickname=temp_nickname,
                gender='M',  # 기본값
                salary='under_30m',
                wealth='under_10m',
                tendency='neutral',
                deposit_amount='under_100k',
                deposit_period='under_6m',
                has_completed_profile=False  # 프로필 미완료 플래그
            )
            token = Token.objects.create(user=user)
            return Response(
                {
                    'status': 'additional_info_required',
                    'key': token.key,
                    'temp_nickname': temp_nickname,
                    'has_completed_profile': user.has_completed_profile,
                },
                status=status.HTTP_202_ACCEPTED
            )
        except IntegrityError:
            return Response(
                {'error': '사용자 생성 실패'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_social_signup(request):
    """
    추가 정보 입력 핸들러
    1. 임시 사용자의 추가 정보 저장
    2. 프로필 완료 상태로 업데이트
    """
    user = request.user
    
    # 1. 이미 프로필 완료된 사용자 차단
    if user.has_completed_profile:
        return Response(
            {'error': '이미 프로필을 완료했습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. 요청 데이터 유효성 검사
    data = request.data
    required_fields = [
        'nickname', 'gender', 'salary', 
        'wealth', 'tendency', 'deposit_amount', 
        'deposit_period'
    ]
    
    # 필수 필드 누락 확인
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return Response(
            {'missing_fields': missing_fields},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3. 닉네임 중복 검사 (변경된 경우에만)
    new_nickname = data['nickname']
    if user.nickname != new_nickname:
        if User.objects.filter(nickname=new_nickname).exists():
            return Response(
                {'nickname': '이미 사용 중인 닉네임입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 4. 사용자 정보 업데이트
    try:
        user.nickname = new_nickname
        user.gender = data['gender']
        user.salary = data['salary']
        user.wealth = data['wealth']
        user.tendency = data['tendency']
        user.deposit_amount = data['deposit_amount']
        user.deposit_period = data['deposit_period']
        user.has_completed_profile = True  # 프로필 완료 플래그 설정
        
        user.save()
        return Response(
            {'status': '프로필이 성공적으로 업데이트되었습니다.'},
            status=status.HTTP_200_OK
        )
    except IntegrityError as e:
        # 데이터베이스 무결성 오류 처리
        return Response(
            {'error': '데이터 저장 중 오류 발생', 'detail': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )