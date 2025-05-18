from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer, UserUpdateSerializer, ChangePasswordSerializer

User = get_user_model()

@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '회원가입 성공'}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)
        return Response({'message': '로그인 성공'}, status=200)
    return Response({'error': '오류'}, status=400)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': '로그아웃 성공'}, status=200)


@api_view(['DELETE'])
def delete_user(request):
    request.user.delete()
    return Response({'message': '탈퇴 완료'}, status=204)


@api_view(['PUT', 'PATCH'])
def update_user(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': '정보 수정 완료'}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not request.user.check_password(serializer.validated_data['old_password']):
            return Response({'error': '기존 비밀번호 틀림'}, status=400)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({'message': '비밀번호 변경 완료'}, status=200)
    return Response(serializer.errors, status=400)