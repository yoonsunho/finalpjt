from rest_framework import serializers
from .models import SavingRoom, SavingParticipant, SavingDeposit
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class SavingDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingDeposit
        fields = ['id', 'amount', 'memo', 'created_at']

class SavingParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total_saved = serializers.SerializerMethodField()

    class Meta:
        model = SavingParticipant
        fields = ['id', 'user', 'joined_at', 'total_saved']

    def get_total_saved(self, obj):
        return obj.total_saved_amount()

class SavingRoomListSerializer(serializers.ModelSerializer):
    achievement_rate = serializers.SerializerMethodField()

    class Meta:
        model = SavingRoom
        fields = ['id', 'name', 'goal_amount', 'achievement_rate']

    def get_achievement_rate(self, obj):
        return obj.achievement_rate()

class SavingRoomDetailSerializer(serializers.ModelSerializer):
    participants = SavingParticipantSerializer(many=True, read_only=True)
    total_saved = serializers.SerializerMethodField()
    achievement_rate = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)  # 변경점: UserSerializer 사용

    class Meta:
        model = SavingRoom
        fields = ['id', 'name', 'description', 'goal_amount', 'deadline', 'created_by', 'created_at', 'total_saved', 'achievement_rate', 'participants']

    def get_total_saved(self, obj):
        return obj.total_saved()

    def get_achievement_rate(self, obj):
        return obj.achievement_rate()

class SavingRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingRoom
        fields = ['id','name', 'description', 'goal_amount', 'deadline']
