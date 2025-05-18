from rest_framework import serializers
from .models import DepositProducts,DepositOptions, SavingProducts, SavingOptions

# deposit
# deposit 데이터 불러오기
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields =('interest_user',)

class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model= DepositOptions
        fields ='__all__'
        read_only_fields = ('deposit_product',)

# saving
class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields='__all__'
        read_only_fields =('interest_user','joined_users',)

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model =SavingOptions
        fields='__all__'
        read_only_fields =('saving_product','joined_users',)
