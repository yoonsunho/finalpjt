from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None     # username필드 제거
    # username = models.CharField(max_length=150, unique=True,)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, unique=True)

    GENDER_CHOICES = [('M', '남성'), ('F', '여성')]
    SALARY_CHOICES = [
        ('under_30m', '3천만원 미만'),
        ('30m_50m', '3천만원~5천만원'),
        ('50m_100m', '5천만원~1억원'),
        ('over_100m', '1억원 이상'),
    ]
    WEALTH_CHOICES = [
        ('under_10m', '1천만원 미만'),
        ('10m_30m', '1천~3천만원'),
        ('30m_50m', '3천~5천만원'),
        ('50m_100m', '5천~1억원'),
        ('over_100m', '1억원 이상'),
    ]
    TENDENCY_CHOICES = [
        ('safe', '안정형'),
        ('neutral', '중립형'),
        ('aggressive', '공격형'),
    ]
    DEPOSIT_AMOUNT_CHOICES = [
        ('under_100k', '10만원 미만'),
        ('100k_500k', '10~50만원'),
        ('500k_1m', '50~100만원'),
        ('over_1m', '100만원 이상'),
    ]
    DEPOSIT_PERIOD_CHOICES = [
        ('under_6m', '6개월 미만'),
        ('6m_12m', '6~12개월'),
        ('1y_2y', '1~2년'),
        ('over_2y', '2년 이상'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    salary = models.CharField(max_length=20, choices=SALARY_CHOICES)
    wealth = models.CharField(max_length=20, choices=WEALTH_CHOICES)
    tendency = models.CharField(max_length=20, choices=TENDENCY_CHOICES)
    deposit_amount = models.CharField(max_length=20, choices=DEPOSIT_AMOUNT_CHOICES)
    deposit_period = models.CharField(max_length=20, choices=DEPOSIT_PERIOD_CHOICES)

    has_completed_profile = models.BooleanField(default=False)  # 필드 추가(소셜로그인)
    
    USERNAME_FIELD = 'email'    # username 필드  email로 변경
    REQUIRED_FIELDS = ['nickname']  # createsuperuser 시 필수

    objects = CustomUserManager()

    def __str__(self):
        return self.email


