# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'password', 'nickname',
            'gender', 'salary', 'wealth', 'tendency',
            'deposit_amount', 'deposit_period'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'nickname', 'gender', 'salary',
            'wealth', 'tendency', 'deposit_amount', 'deposit_period'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
