from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomRegisterSerializer(RegisterSerializer):
    # username 필드 제거, email은 기본 제공
    nickname = serializers.CharField(max_length=20,required=True)
    gender = serializers.ChoiceField(
        choices=[('M', '남성'), ('F', '여성')], required=True
    )
    salary = serializers.ChoiceField(
        choices=[
            ('under_30m', '3천만원 미만'),
            ('30m_50m', '3천만원~5천만원'),
            ('50m_100m', '5천만원~1억원'),
            ('over_100m', '1억원 이상'),
        ],
        required=True
    )
    wealth = serializers.ChoiceField(
        choices=[
            ('under_10m', '1천만원 미만'),
            ('10m_30m', '1천~3천만원'),
            ('30m_50m', '3천~5천만원'),
            ('50m_100m', '5천~1억원'),
            ('over_100m', '1억원 이상'),
        ],
        required=True
    )
    tendency = serializers.ChoiceField(
        choices=[
            ('safe', '안정형'),
            ('neutral', '중립형'),
            ('aggressive', '공격형'),
        ],
        required=True
    )
    deposit_amount = serializers.ChoiceField(
        choices=[
            ('under_100k', '10만원 미만'),
            ('100k_500k', '10~50만원'),
            ('500k_1m', '50~100만원'),
            ('over_1m', '100만원 이상'),
        ],
        required=True
    )
    deposit_period = serializers.ChoiceField(
        choices=[
            ('under_6m', '6개월 미만'),
            ('6m_12m', '6~12개월'),
            ('1y_2y', '1~2년'),
            ('over_2y', '2년 이상'),
        ],
        required=True
    )

    def get_cleaned_data(self):
        # 기본 필드(이메일, 비밀번호) + 커스텀 필드 병합
        base_data = super().get_cleaned_data()
        custom_data = {
            'nickname': self.validated_data.get('nickname'),
            'gender': self.validated_data.get('gender'),
            'salary': self.validated_data.get('salary'),
            'wealth': self.validated_data.get('wealth'),
            'tendency': self.validated_data.get('tendency'),
            'deposit_amount': self.validated_data.get('deposit_amount'),
            'deposit_period': self.validated_data.get('deposit_period'),
        }
        return {**base_data, **custom_data} 


    def save(self, request):
        user = super().save(request)    # allauth내부 로직 실행
        # 사용자 생성 로직
        user.nickname = self.validated_data.get('nickname')
        user.gender = self.validated_data.get('gender')
        user.salary = self.validated_data.get('salary')
        user.wealth = self.validated_data.get('wealth')
        user.tendency = self.validated_data.get('tendency')
        user.deposit_amount = self.validated_data.get('deposit_amount')
        user.deposit_period = self.validated_data.get('deposit_period')
        user.save()
        return user
        

# 마이페이지에 띄울 내 프로필 정보
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'nickname', 'gender', 'salary', 'wealth', 
            'tendency', 'deposit_amount', 'deposit_period'
        ]