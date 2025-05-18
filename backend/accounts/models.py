from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, unique=True)

    # 성별
    GENDER_CHOICES = [
      (1, 'Male'),
      (2, 'Female'),
      ]
      
    # 소득 / 월급으로 ? 연봉으로? 
    SALARY_CHOICES = [
      (1, '250만원 이하'),
      (2, '250만원 이상 ~ 300만원 이하'),
      (3, '300만원 이상 ~ 400만원 이하'),
      (4, '400만원 이상 ~ 500만원 이하'),
      (5, '500만원 이상'),
    ]

    # 자산
    WEALTH_CHOICES = [
      (1, '1천만원 이하'),
      (2, '1천만 ~ 5천만'),
      (3, '5천만 ~ 1억'),
      (4, '1억 ~ 3억'),
      (5, '3억 이상'),
    ]

    # 투자성향
    TENDENCY_CHOICES = [
      (1, '안정형'),    
      (2, '중립형'),    
      (3, '공격형'),      
    ]

    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES)
    salary = models.PositiveIntegerField(choices=SALARY_CHOICES)
    wealth = models.PositiveIntegerField(choices=WEALTH_CHOICES)
    tendency = models.PositiveIntegerField(choices=TENDENCY_CHOICES)

    # 희망 저축금액 / 최소 1만원
    deposit_amount = models.PositiveIntegerField(
        validators=[MinValueValidator(10000)]
        )

    # 희망 저축기간 / 최소 1개월
    deposit_period = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    objects = UserManager()

    def __str__(self):
        return self.nickname