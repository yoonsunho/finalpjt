from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


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
        
         # ✅ 일반 회원가입은 프로필 완료 상태로 설정
        user.has_completed_profile = True
        
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

# 회원정보 수정에 사용할 serializer
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only = True) # 이메일은 수정 불가

    class Meta:
        model = CustomUser
        fields = (  'email', 'nickname', 'gender', 'salary', 'wealth', 
            'tendency', 'deposit_amount', 'deposit_period')
    
    def validate_nickname(self,value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value
    
# 비밀번호 수정 
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("새 비밀번호와 확인 비밀번호가 일치하지 않습니다.")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 틀렸습니다.")
        return value
    
class SocialSignupCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'nickname', 'gender', 'salary', 'wealth', 
            'tendency', 'deposit_amount', 'deposit_period'
        ]
