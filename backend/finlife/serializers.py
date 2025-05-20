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
    
    # 인라인 방식으로 변경(option에서 읽어올 product정보)
    deposit_product = serializers.SerializerMethodField()
    
    class Meta:
        model = DepositOptions
        fields =('id','save_trm','intr_rate2','deposit_product',)
    
    def get_deposit_product(self, obj):
        return {
            "kor_co_nm": obj.deposit_product.kor_co_nm,
            "fin_prdt_nm": obj.deposit_product.fin_prdt_nm
        }
    

class DepositDetailSerializer(serializers.ModelSerializer):

    deposit_product = DepositProductsSerializer(read_only=True)
        
    class Meta:
        model = DepositOptions
        fields = '__all__'
        
        
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
