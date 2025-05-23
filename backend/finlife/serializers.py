from rest_framework import serializers
from .models import DepositProducts,DepositOptions, SavingProducts, SavingOptions

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
    max_intr_rate2 = serializers.SerializerMethodField()
    intr_rate_type_nm = serializers.SerializerMethodField()  

    
    class Meta:
        model = DepositProducts
        fields = (
            'id',
            'kor_co_nm',
            'fin_prdt_nm',
            'max_intr_rate2',
            'intr_rate_type_nm',
        )
        
    def get_max_intr_rate2(self,obj):
        
        option = obj.depositoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate2 if option else None
    
    def get_intr_rate_type_nm(self, obj):
        option = obj.depositoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate_type_nm if option else None
    
    

class DepositDetailSerializer(serializers.ModelSerializer):
    
    options = DepositOptionsSerializer(
        source='depositoptions_set',  # ✅ 모델 관계명 (기본값: depositoptions_set)
        many=True,
        read_only=True
    )
        
    class Meta:
        model = DepositProducts
        fields = '__all__'          # # 모든 필드 + options + max_intr_rate2
        
        
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
    
    class Meta:
        model = SavingProducts
        fields = (
            'id',
            'kor_co_nm',
            'fin_prdt_nm',
            'max_intr_rate2',
            'intr_rate_type_nm',
        )
        
    def get_max_intr_rate2(self, obj):
        option = obj.savingoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate2 if option else None

    def get_intr_rate_type_nm(self, obj):
        option = obj.savingoptions_set.order_by('-intr_rate2').first()
        return option.intr_rate_type_nm if option else None

        
    

class SavingDetailSerializer(serializers.ModelSerializer):

    options = SavingOptionsSerializer(
        source='savingoptions_set',  # 기본 related_name
        many=True,
        read_only=True
    )

    class Meta:
        model = SavingProducts
        fields = '__all__'  # 모든 상품 필드 + options