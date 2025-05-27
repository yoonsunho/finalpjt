from django.db import models
from django.conf import settings
from django.db.models import Max

from django.utils import timezone

# Create your models here.
# 예금
class DepositProducts(models.Model):
    interest_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='DepositInterest',  # 추가
        related_name='interest_deposits',
        blank=True)       # 찜하기 누른 사용자
    joined_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='DepositJoin',
        related_name='joined_deposits',
        blank=True)
    dcls_month = models.TextField() # 공시 제출월 [YYYYMM]
    
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField()  # 금융 회사 명
    fin_prdt_cd = models.TextField(unique=True) # 금융 상품 코드
    fin_prdt_nm = models.TextField()    # 금융 상품 명
    join_way = models.TextField()   # 가입 방법
    mtrt_int = models.TextField()   # 만기후 이자율
    spcl_cnd = models.TextField()   # 우대 조건
    join_deny = models.IntegerField(default=0)  # 가입 제한(1.제한 없음, 2: 서면전용, 3: 일부제한)
    etc_note = models.TextField()   # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)  # 최고한도

    def max_rate(self):
        return self.depositoptions_set.aggregate(max_rate=Max('intr_rate2'))['max_rate']

    

    
class DepositOptions(models.Model):
    deposit_product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 예금 상품 id 포린키
    intr_rate_type = models.CharField(max_length=100) # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축 금리 유형명
    save_trm = models.IntegerField()    # 저축기간(단위: 개월)
    intr_rate = models.FloatField(null=True) # 저축금리
    intr_rate2 = models.FloatField(null=True)    # 최고 우대 금리
    

# 적금
class SavingProducts(models.Model):
    interest_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='SavingInterest',
        related_name='interest_savings',
        blank=True
    )    # 적금 상품 찜한 user
    joined_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='SavingJoin',
        related_name='joined_savings',
        blank=True
    )   # 실제 가입자

    dcls_month = models.TextField() # 공시 제출월 [YYYYMM]
    fin_co_no = models.TextField()  # 금융회사 코드
    kor_co_nm = models.TextField() # 금융회사 명
    fin_prdt_cd = models.TextField()    # 금융상품 코드
    fin_prdt_nm = models.TextField()    # 금융 상품명
    join_way = models.TextField()   # 가입 방법
    mtrt_int = models.TextField()   # 만기 후 이자율
    spcl_cnd = models.TextField()   # 우대조건
    join_deny = models.IntegerField(default=0) # 가입제한 Ex) 1:제한없음, 2:서민전용, 3:일부제한
    etc_note = models.TextField()   # 기타 유의사항
    max_limit = models.IntegerField(blank=True, null=True)   # 최고한도

    def max_rate(self):
        return self.savingoptions_set.aggregate(max_rate=Max('intr_rate2'))['max_rate']

class SavingOptions(models.Model):

    saving_product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)    # 적금 id포린키
    intr_rate_type = models.CharField(max_length=100)   # 저축 금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)    # 저축 금리 유형명
    rsrv_type = models.TextField()  # 적립 유형
    rsrv_type_nm = models.TextField()   # 적립 유형명
    save_trm = models.IntegerField()    # 저축 기간 [단위: 개월]
    intr_rate = models.FloatField(null=True)    # 저축 금리 [소수점 2자리]
    intr_rate2 = models.FloatField(null=True)   # 최고 우대금리 [소수점 2자리]
    

# 찜하기 기능
class DepositInterest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'product')  # 중복 찜하기 방지
        db_table = 'deposit_interest'

class SavingInterest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'product')
        db_table = 'saving_interest'
        
# 가입 기능
class DepositJoin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'product')  # 중복 찜하기 방지
        db_table = 'deposit_join'
        
class SavingJoin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'product')
        db_table = 'saving_join'
        
        
