from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, unique=True)

    GENDER_CHOICES = [('M', '남성'), ('F', '여성')]
    SALARY_CHOICES = [(1, '3천만원 미만'), (2, '3~5천'), (3, '5천~1억'), (4, '1억 이상')]
    WEALTH_CHOICES = [(1, '1천 미만'), (2, '1천~3천'), (3, '3천~5천'), (4, '5천~1억'), (5, '1억 이상')]
    TENDENCY_CHOICES = [(1, '안정형'), (2, '중립형'), (3, '공격형')]
    DEPOSIT_AMOUNT_CHOICES = [(1, '10만원 미만'), (2, '10~50'), (3, '50~100'), (4, '100 이상')]
    DEPOSIT_PERIOD_CHOICES = [(1, '6개월 미만'), (2, '6~12개월'), (3, '1~2년'), (4, '2년 이상')]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    salary = models.IntegerField(choices=SALARY_CHOICES, null=True)
    wealth = models.IntegerField(choices=WEALTH_CHOICES, null=True)
    tendency = models.IntegerField(choices=TENDENCY_CHOICES, null=True)
    deposit_amount = models.IntegerField(choices=DEPOSIT_AMOUNT_CHOICES, null=True)
    deposit_period = models.IntegerField(choices=DEPOSIT_PERIOD_CHOICES, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nickname']

    def __str__(self):
        return self.username
