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
    depositoptions_set = serializers.SerializerMethodField()

    class Meta:
        model = DepositProducts
        fields = (
            'id', 
            'kor_co_nm', 
            'fin_prdt_nm', 
            'join_way', 
            'depositoptions_set'  # 커스텀 필드
        )
    
    def get_depositoptions_set(self, obj):
        # 옵션에서 save_trm, intr_rate2만 추출
        options = obj.depositoptions_set.all()
        return [
            {"save_trm": opt.save_trm, "intr_rate2": opt.intr_rate2}
            for opt in options
        ]
    

class DepositDetailSerializer(serializers.ModelSerializer):

    depositoptions_set = DepositOptionsSerializer(many=True, read_only=True)
    
    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields =('interest_users','joined_users',)
        
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
