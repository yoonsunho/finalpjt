from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User

class SignUpSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
    salary = serializers.IntegerField(required=True)
    wealth = serializers.IntegerField(required=True)
    tendency = serializers.IntegerField(required=True)
    deposit_amount = serializers.IntegerField(required=True)
    deposit_period = serializers.IntegerField(required=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def custom_signup(self, request, user):
        user.email = self.validated_data.get('email')
        user.nickname = self.validated_data.get('nickname')
        user.gender = self.validated_data.get('gender')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.tendency = self.validated_data.get('tendency')
        user.deposit_amount = self.validated_data.get('deposit_amount')
        user.deposit_period = self.validated_data.get('deposit_period')
        user.save()

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        extra_fields = ['username', 'email', 'nickname', 'gender', 'salary', 'wealth', 'tendency', 'deposit_amount', 'deposit_period']
        for field in extra_fields:
            data[field] = self.validated_data.get(field)
        return data
