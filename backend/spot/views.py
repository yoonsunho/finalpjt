from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import GoldPrice, SilverPrice
from .serializers import GoldPriceSerializer, SilverPriceSerializer

@api_view(['GET'])
def commodity_price(request):
    """
    금 또는 은 중 하나의 가격 데이터 반환
    - asset: 'gold' (기본값) 또는 'silver' 
    - start_date, end_date: 기간 필터링 (없으면 전체 기간)
    """
    # 쿼리 파라미터 받기
    asset = request.GET.get('asset', 'gold')         # 기본값: 금
    start_date = request.GET.get('start_date')        # 예: '2024-01-01'  
    end_date = request.GET.get('end_date')            # 예: '2024-12-31'

    # 자산 선택에 따른 쿼리셋과 시리얼라이저 결정
    if asset == 'gold':
        queryset = GoldPrice.objects.all()
        serializer_class = GoldPriceSerializer
        asset_name = '금'
    elif asset == 'silver':
        queryset = SilverPrice.objects.all()
        serializer_class = SilverPriceSerializer
        asset_name = '은'
    else:
        return Response(
            {'error': '유효하지 않은 자산 타입입니다. (gold 또는 silver만 허용)'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 날짜 필터링 (있으면 적용, 없으면 전체 기간)
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    # 데이터 시리얼라이즈
    serializer = serializer_class(queryset, many=True)
    
    # 응답 데이터 구성
    return Response({
        'asset': asset,
        'asset_name': asset_name,
        'data': serializer.data,
        'period': {
            'start_date': start_date or '전체 기간',
            'end_date': end_date or '전체 기간'
        },
        'total_count': len(serializer.data)
    })