# savingroom/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import SavingRoom, SavingParticipant, SavingDeposit
from .serializers import (
    SavingRoomListSerializer,
    SavingRoomDetailSerializer,
    SavingRoomCreateSerializer,
    SavingDepositSerializer
)

# 방 목록 조회 & 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def room_list(request):
    if request.method == 'GET':
        rooms = SavingRoom.objects.all()
        serializer = SavingRoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SavingRoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 방 상세 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_detail(request, room_id):

    room = get_object_or_404(
        SavingRoom.objects.prefetch_related('participants__deposits'), 
        id=room_id
    )
    
    serializer = SavingRoomDetailSerializer(room)
    return Response(serializer.data)

# 방 참가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_room(request, room_id):
    room = get_object_or_404(SavingRoom, id=room_id)
    user = request.user

    if SavingParticipant.objects.filter(room=room, user=user).exists():
        return Response({'detail': '이미 참가한 방입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    SavingParticipant.objects.create(room=room, user=user)
    return Response({'detail': '참가 완료!'}, status=status.HTTP_201_CREATED)

# 입금
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_deposit(request, room_id):
    room = get_object_or_404(SavingRoom, id=room_id)
    user = request.user
    amount = request.data.get('amount')
    memo = request.data.get('memo', '')

    if not amount:
        return Response({'detail': '금액을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        participant = SavingParticipant.objects.get(room=room, user=user)
    except SavingParticipant.DoesNotExist:
        return Response({'detail': '먼저 참가해야 저축할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = int(amount)
    except ValueError:
        return Response({'detail': '유효하지 않은 금액입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    deposit = SavingDeposit.objects.create(participant=participant, amount=amount, memo=memo)
    serializer = SavingDepositSerializer(deposit)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_created_rooms(request):
    user = request.user
    rooms = SavingRoom.objects.filter(created_by=user)
    serializer = SavingRoomListSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_joined_rooms(request):
    user = request.user
    participants = SavingParticipant.objects.filter(user=user)
    rooms = [p.room for p in participants]
    serializer = SavingRoomListSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_all_rooms(request):
    user = request.user
    created_rooms = SavingRoom.objects.filter(created_by=user)
    joined_rooms = SavingRoom.objects.filter(participants__user=user)
    all_rooms = created_rooms.union(joined_rooms)
    serializer = SavingRoomListSerializer(all_rooms, many=True)
    return Response(serializer.data)