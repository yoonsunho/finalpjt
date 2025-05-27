# comsumers.py
# websocket (실시간 입금 내역)
# AsyncWebsocketConsumer로 실시간 입금 내역 전송
#참가자 예외처리, 인증 체크, 그룹 브로드캐스트 등 Channels의 베스트 프랙티스 적용
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import SavingRoom, SavingParticipant, SavingDeposit
from django.core.exceptions import ObjectDoesNotExist  # 추가


class SavingRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'saving_room_{self.room_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        if user.is_anonymous:
            await self.close(code=4001)
            return

        amount = int(data['amount'])
        memo = data.get('memo', '')

        try:
            await self.save_deposit(user, amount, memo)
        except ObjectDoesNotExist:  # 예외 처리 추가
            await self.send(text_data=json.dumps({
                'error': '이 방에 참가하지 않았습니다.'
            }))
            return
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_deposit',
                'nickname': user.nickname,
                'amount': amount,
                'memo': memo
            }
        )

    async def send_deposit(self, event):
        await self.send(text_data=json.dumps({
            'nickname': event['nickname'],
            'amount': event['amount'],
            'memo': event['memo']
        }))

    @database_sync_to_async
    def save_deposit(self, user, amount, memo):
        
        try:
            participant = SavingParticipant.objects.get(  # get → try-except로 감쌈
                room_id=self.room_id, 
                user=user
            )
        except SavingParticipant.DoesNotExist:
            
            raise ObjectDoesNotExist("참가자가 존재하지 않습니다")  # 예외 전파

        SavingDeposit.objects.create(
            participant=participant, 
            amount=amount, 
            memo=memo
        )