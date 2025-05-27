# consumers.py - Fixed version with better authentication handling
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import SavingRoom, SavingParticipant, SavingDeposit
import logging

logger = logging.getLogger(__name__)

class SavingRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room ID from URL
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'saving_room_{self.room_id}'
        
        # Check authentication first
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            logger.warning(f"Anonymous user attempted to connect to room {self.room_id}")
            await self.close(code=4001)  # Unauthorized
            return
        
        # Check if user is participant in this room
        try:
            is_participant = await self.check_user_participation(user, self.room_id)
            if not is_participant:
                logger.warning(f"User {user.nickname} is not a participant in room {self.room_id}")
                await self.close(code=4003)  # Forbidden
                return
        except Exception as e:
            logger.error(f"Error checking participation: {e}")
            await self.close(code=4000)  # Bad request
            return
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        # Accept the WebSocket connection
        await self.accept()
        logger.info(f"User {user.nickname} connected to room {self.room_id}")

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        user = self.scope.get('user')
        if user and not user.is_anonymous:
            logger.info(f"User {user.nickname} disconnected from room {self.room_id} with code {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': '잘못된 JSON 형식입니다.'
            }))
            return
        
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            await self.send(text_data=json.dumps({
                'error': '인증이 필요합니다.'
            }))
            return

        # Validate required fields
        if 'amount' not in data:
            await self.send(text_data=json.dumps({
                'error': '금액을 입력해주세요.'
            }))
            return
        
        try:
            amount = int(data['amount'])
            if amount <= 0:
                await self.send(text_data=json.dumps({
                    'error': '금액은 0보다 커야 합니다.'
                }))
                return
        except (ValueError, TypeError):
            await self.send(text_data=json.dumps({
                'error': '올바른 금액을 입력해주세요.'
            }))
            return

        memo = data.get('memo', '').strip()
        if len(memo) > 100:  # Limit memo length
            await self.send(text_data=json.dumps({
                'error': '메모는 100자 이하로 입력해주세요.'
            }))
            return

        try:
            # Save deposit to database
            await self.save_deposit(user, amount, memo)
            
            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_deposit',
                    'nickname': user.nickname,
                    'amount': amount,
                    'memo': memo
                }
            )
            
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'error': '이 방에 참가하지 않았습니다.'
            }))
        except Exception as e:
            logger.error(f"Error saving deposit: {e}")
            await self.send(text_data=json.dumps({
                'error': '저축 중 오류가 발생했습니다.'
            }))

    async def send_deposit(self, event):
        """Handle broadcast message from group"""
        await self.send(text_data=json.dumps({
            'type': 'deposit',
            'nickname': event['nickname'],
            'amount': event['amount'],
            'memo': event['memo']
        }))

    @database_sync_to_async
    def check_user_participation(self, user, room_id):
        """Check if user is a participant in the room"""
        try:
            participant = SavingParticipant.objects.get(
                room_id=room_id, 
                user=user
            )
            return True
        except SavingParticipant.DoesNotExist:
            return False

    @database_sync_to_async
    def save_deposit(self, user, amount, memo):
        """Save deposit to database"""
        try:
            participant = SavingParticipant.objects.get(
                room_id=self.room_id, 
                user=user
            )
        except SavingParticipant.DoesNotExist:
            raise ObjectDoesNotExist("참가자가 존재하지 않습니다")

        SavingDeposit.objects.create(
            participant=participant, 
            amount=amount, 
            memo=memo
        )

# # comsumers.py
# # websocket (실시간 입금 내역)
# # AsyncWebsocketConsumer로 실시간 입금 내역 전송
# #참가자 예외처리, 인증 체크, 그룹 브로드캐스트 등 Channels의 베스트 프랙티스 적용
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import SavingRoom, SavingParticipant, SavingDeposit
# from django.core.exceptions import ObjectDoesNotExist  # 추가


# class SavingRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'saving_room_{self.room_id}'

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         user = self.scope['user']
#         if user.is_anonymous:
#             await self.close(code=4001)
#             return

#         amount = int(data['amount'])
#         memo = data.get('memo', '')

#         try:
#             await self.save_deposit(user, amount, memo)
#         except ObjectDoesNotExist:  # 예외 처리 추가
#             await self.send(text_data=json.dumps({
#                 'error': '이 방에 참가하지 않았습니다.'
#             }))
#             return
        
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'send_deposit',
#                 'nickname': user.nickname,
#                 'amount': amount,
#                 'memo': memo
#             }
#         )

#     async def send_deposit(self, event):
#         await self.send(text_data=json.dumps({
#             'nickname': event['nickname'],
#             'amount': event['amount'],
#             'memo': event['memo']
#         }))

#     @database_sync_to_async
#     def save_deposit(self, user, amount, memo):
        
#         try:
#             participant = SavingParticipant.objects.get(  # get → try-except로 감쌈
#                 room_id=self.room_id, 
#                 user=user
#             )
#         except SavingParticipant.DoesNotExist:
            
#             raise ObjectDoesNotExist("참가자가 존재하지 않습니다")  # 예외 전파

#         SavingDeposit.objects.create(
#             participant=participant, 
#             amount=amount, 
#             memo=memo
#         )