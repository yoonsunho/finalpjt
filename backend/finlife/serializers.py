from rest_framework import serializers
from .models import DepositProducts,DepositOptions, SavingProducts, SavingOptions, DepositJoin, DepositInterest, SavingInterest, SavingJoin
from django.db.models import Max
# deposit
# deposit 데이터 불러오기
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields =('interest_users','joined_users',)

class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model= DepositOptions
        fields ='__all__'
        read_only_fields = ('deposit_product',)

# 전체 리스트에 띄울애들
class DepositListSerializer(serializers.ModelSerializer):
    
    # 옵션 중 최대 우대 금리
    # 정렬 필드 최적화
    max_intr_rate2 = serializers.SerializerMethodField(method_name='get_max_rate')
    intr_rate_type_nm = serializers.SerializerMethodField(method_name='get_rate_type')  
    is_interested = serializers.SerializerMethodField()  # 찜하기 상태
    is_joined = serializers.SerializerMethodField()     # 가입 상태
    joined_count = serializers.IntegerField(read_only=True)       # annotate로 전달된 필드
    interest_count = serializers.IntegerField(read_only=True)     # annotate로 전달된 필드

    
    class Meta:
        model = DepositProducts
        fields = (
            'id',
            'kor_co_nm',
            'fin_prdt_nm',
            'max_intr_rate2',
            'intr_rate_type_nm',
            'is_interested',
            'is_joined',
            'interest_count',
            'joined_count',
        )
        
    def get_max_rate(self, obj):
        return obj.depositoptions_set.aggregate(Max('intr_rate2'))['intr_rate2__max']

    def get_rate_type(self, obj):
        options = obj.depositoptions_set.all()
        return options[0].intr_rate_type_nm if options else None
    
    def get_is_interested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DepositInterest.objects.filter(user=request.user, product=obj).exists()
        return False
    
    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DepositJoin.objects.filter(user=request.user, product=obj).exists()
        return False


class DepositDetailSerializer(serializers.ModelSerializer):
    
    options = DepositOptionsSerializer(
        source='depositoptions_set',  # ✅ 모델 관계명 (기본값: depositoptions_set)
        many=True,
        read_only=True
    )
    
    is_interested = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    joined_count = serializers.IntegerField(read_only=True)
    interest_count = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = DepositProducts
        fields = '__all__'          # # 모든 필드 + options + max_intr_rate2
        
    def get_is_interested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DepositInterest.objects.filter(user=request.user, product=obj).exists()
        return False

    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return DepositJoin.objects.filter(user=request.user, product=obj).exists()
        return False
        
        
# saving
class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields='__all__'
        read_only_fields =('interest_users','joined_users',)

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model =SavingOptions
        fields='__all__'
        read_only_fields =('saving_product',)


# 전체 리스트에 띄울애들
class SavingListSerializer(serializers.ModelSerializer):
    
    max_intr_rate2 = serializers.SerializerMethodField()
    intr_rate_type_nm = serializers.SerializerMethodField()  
    is_interested = serializers.SerializerMethodField()  # 찜하기 상태
    is_joined = serializers.SerializerMethodField()     # 가입 상태
    joined_count = serializers.IntegerField(read_only=True)       # annotate로 전달된 필드
    interest_count = serializers.IntegerField(read_only=True)     # annotate로 전달된 필드

 
    
    class Meta:
        model = SavingProducts
        fields = (
            'id',
            'kor_co_nm',
            'fin_prdt_nm',
            'max_intr_rate2',
            'intr_rate_type_nm',
            'is_interested',
            'is_joined',
            'interest_count',
            'joined_count',
        )
        
    def get_max_intr_rate2(self, obj):
        option = obj.savingoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate2 if option else None

    def get_intr_rate_type_nm(self, obj):
        option = obj.savingoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate_type_nm if option else None

        
    def get_is_interested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavingInterest.objects.filter(user=request.user, product=obj).exists()
        return False
    
    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavingJoin.objects.filter(user=request.user, product=obj).exists()
        return False
    


class SavingDetailSerializer(serializers.ModelSerializer):

    options = SavingOptionsSerializer(
        source='savingoptions_set',  # 기본 related_name
        many=True,
        read_only=True
    )
    
    is_interested = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    joined_count = serializers.IntegerField(read_only=True)
    interest_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SavingProducts
        fields = '__all__'  # 모든 상품 필드 + options
        
    def get_is_interested(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavingInterest.objects.filter(user=request.user, product=obj).exists()
        return False

    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavingJoin.objects.filter(user=request.user, product=obj).exists()
        return False
        
        
# 찜하기 serializer
class DepositInterestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    company_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    
    class Meta:
        model = DepositInterest
        fields = ['id', 'user', 'product', 'created_at', 'product_name', 'company_name']
        read_only_fields = ['user', 'created_at']

class SavingInterestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    company_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    
    class Meta:
        model = SavingInterest
        fields = ['id', 'user', 'product', 'created_at', 'product_name', 'company_name']
        read_only_fields = ['user', 'created_at']

# 가입하기 serializer
class DepositJoinSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    company_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    
    class Meta:
        model = DepositJoin
        fields = ['id', 'user', 'product', 'joined_at', 'product_name', 'company_name']
        read_only_fields = ['user', 'joined_at']

class SavingJoinSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    company_name = serializers.CharField(source='product.kor_co_nm', read_only=True)
    
    class Meta:
        model = SavingJoin
        fields = ['id', 'user', 'product', 'joined_at', 'product_name', 'company_name']
        read_only_fields = ['user', 'joined_at']