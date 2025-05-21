from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
# from .models import User

class CustomRegisterSerializer(RegisterSerializer):
    # username 필드 제거, email은 기본 제공
    nickname = serializers.CharField(max_length=20)
    gender = serializers.ChoiceField(choices=[('M', '남성'), ('F', '여성')], required=False, allow_null=True)
    salary = serializers.ChoiceField(choices=[(1, '3천만원 미만'), (2, '3~5천'), (3, '5천~1억'), (4, '1억 이상')], required=False, allow_null=True)
    wealth = serializers.ChoiceField(choices=[(1, '1천 미만'), (2, '1천~3천'), (3, '3천~5천'), (4, '5천~1억'), (5, '1억 이상')], required=False, allow_null=True)
    tendency = serializers.ChoiceField(choices=[(1, '안정형'), (2, '중립형'), (3, '공격형')], required=False, allow_null=True)
    deposit_amount = serializers.ChoiceField(choices=[(1, '10만원 미만'), (2, '10~50'), (3, '50~100'), (4, '100 이상')], required=False, allow_null=True)
    deposit_period = serializers.ChoiceField(choices=[(1, '6개월 미만'), (2, '6~12개월'), (3, '1~2년'), (4, '2년 이상')], required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['gender'] = self.validated_data.get('gender', None)
        data['salary'] = self.validated_data.get('salary', None)
        data['wealth'] = self.validated_data.get('wealth', None)
        data['tendency'] = self.validated_data.get('tendency', None)
        data['deposit_amount'] = self.validated_data.get('deposit_amount', None)
        data['deposit_period'] = self.validated_data.get('deposit_period', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data.get('nickname')
        user.gender = self.cleaned_data.get('gender')
        user.salary = self.cleaned_data.get('salary')
        user.wealth = self.cleaned_data.get('wealth')
        user.tendency = self.cleaned_data.get('tendency')
        user.deposit_amount = self.cleaned_data.get('deposit_amount')
        user.deposit_period = self.cleaned_data.get('deposit_period')
        user.save()
        return user

# class SignUpSerializer(RegisterSerializer):
#     email = serializers.EmailField(required=True)
#     nickname = serializers.CharField(required=True)
#     gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
#     salary = serializers.IntegerField(required=True)
#     wealth = serializers.IntegerField(required=True)
#     tendency = serializers.IntegerField(required=True)
#     deposit_amount = serializers.IntegerField(required=True)
#     deposit_period = serializers.IntegerField(required=True)

#     def validate_username(self, value):
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
#         return value

#     def validate_nickname(self, value):
#         if User.objects.filter(nickname=value).exists():
#             raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
#         return value

#     def custom_signup(self, request, user):
#         user.email = self.validated_data.get('email')
#         user.nickname = self.validated_data.get('nickname')
#         user.gender = self.validated_data.get('gender')
#         user.salary = self.validated_data.get('salary')
#         user.wealth = self.validated_data.get('wealth')
#         user.tendency = self.validated_data.get('tendency')
#         user.deposit_amount = self.validated_data.get('deposit_amount')
#         user.deposit_period = self.validated_data.get('deposit_period')
#         user.save()

#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()
#         extra_fields = ['username', 'email', 'nickname', 'gender', 'salary', 'wealth', 'tendency', 'deposit_amount', 'deposit_period']
#         for field in extra_fields:
#             data[field] = self.validated_data.get(field)
#         return data
