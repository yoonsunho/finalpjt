from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods,require_POST
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositInterest, DepositJoin, SavingInterest, SavingJoin
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositListSerializer ,DepositDetailSerializer, SavingProductsSerializer, SavingOptionsSerializer, SavingListSerializer, SavingDetailSerializer, DepositJoinSerializer, DepositInterestSerializer, SavingJoinSerializer, SavingInterestSerializer

# Permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['GET',])
def get_deposit_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'

    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(BASE_URL, params = params).json()['result']
   
    deposit_baselist = response['baseList']
    deposit_optionlist = response['optionList']

    # 상품 정보 저장 및 직렬화
    for base in deposit_baselist:
        if DepositProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']):
            continue
        deposit_product = {
            'dcls_month' : base.get('dcls_month'),
            'fin_prdt_cd': base.get('fin_prdt_cd'),
            'fin_co_no': base.get('fin_co_no'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'join_way': base.get('join_way'),
            'mtrt_int': base.get('mtrt_int'),
            'spcl_cnd': base.get('spcl_cnd'),
            'join_deny': base.get('join_deny'),
            'etc_note': base.get('etc_note'),
            'max_limit': base.get('max_limit')
        }
        serializer = DepositProductsSerializer(data=deposit_product)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        
    # deposit 옵션 정보 저장 및 직렬화
    for opt in deposit_optionlist:
        prdt_cd = opt['fin_prdt_cd']
        products = DepositProducts.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            deposit_option = {
                'intr_rate_type': opt.get('intr_rate_type'),
                'intr_rate_type_nm': opt.get('intr_rate_type_nm'),
                'save_trm': opt.get('save_trm'),
                'intr_rate': opt.get('intr_rate'),
                'intr_rate2': opt.get('intr_rate2'),
            }
            serializer = DepositOptionsSerializer(data=deposit_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_product = product)
    return Response('데이터 가져오기 성공!!')

# 적금 saving ====================================
@api_view(['GET'])
def get_saving_products(request):
    
    BASE_URL ='http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

    params = {
        'auth': settings.FIN_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    
    response = requests.get(BASE_URL, params = params).json()['result']
   
    saving_baselist = response['baseList']
    saving_optionlist = response['optionList']

    # 상품 정보 저장 및 직렬화
    for base in saving_baselist:
        if SavingProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']):
            continue
        saving_product = {
            'dcls_month' : base['dcls_month'],
            'fin_co_no': base['fin_co_no'],
            'kor_co_nm': base['kor_co_nm'],
            'fin_prdt_cd': base['fin_prdt_cd'],
            'fin_prdt_nm': base['fin_prdt_nm'],
            'join_way': base['join_way'],
            'mtrt_int': base['mtrt_int'],
            'spcl_cnd': base['spcl_cnd'],
            'join_deny': base['join_deny'],
            'etc_note': base['etc_note'],
            'max_limit': base['max_limit']
        }
        serializer = SavingProductsSerializer(data=saving_product)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        
    # saving 옵션 정보 저장 및 직렬화
    for opt in saving_optionlist:
        prdt_cd = opt['fin_prdt_cd']
        products =  SavingProducts.objects.filter(fin_prdt_cd=prdt_cd)
        for product in products:
            saving_option = {
                'intr_rate_type': opt.get('intr_rate_type'),
                'intr_rate_type_nm': opt.get('intr_rate_type_nm'),
                'rsrv_type': opt.get('rsrv_type'),
                'rsrv_type_nm': opt.get('rsrv_type_nm'),
                'save_trm': opt.get('save_trm'),
                'intr_rate': opt.get('intr_rate'),
                'intr_rate2': opt.get('intr_rate2'),  
            }
            serializer = SavingOptionsSerializer(data=saving_option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_product = product)
    return Response('데이터 가져오기 성공!')

# 예금 리스트 조회
@api_view(['GET'])
def deposit_product_list(request):
    queryset = DepositProducts.objects.all().annotate(
        interest_count=Count('interest_users', distinct=True),
        joined_count=Count('joined_users', distinct=True)
    )

    # 검색 기능 추가
    search_term = request.query_params.get('search')
    if search_term:
        queryset = queryset.filter(fin_prdt_nm__icontains = search_term)

    # 필터링
    intr_rate_type_nm = request.query_params.get('intr_rate_type_nm')
    kor_co_nm = request.query_params.get('kor_co_nm')
    if intr_rate_type_nm:
        queryset = queryset.filter(depositoptions__intr_rate_type_nm=intr_rate_type_nm)
    if kor_co_nm:
        queryset = queryset.filter(kor_co_nm__icontains=kor_co_nm)

    # 정렬
    ordering = request.query_params.get('ordering')
    allowed_ordering = ['interest_count', '-interest_count', 'joined_count', '-joined_count']
    if ordering in allowed_ordering:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('id')  # 기본 정렬

    serializer = DepositListSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_detail(request, product_id):
    product = get_object_or_404(
        DepositProducts.objects
        .prefetch_related('depositoptions_set')
        .annotate(
            joined_count=Count('joined_users', distinct=True),
            interest_count=Count('interest_users', distinct=True)
        ),
        id=product_id
    )
    serializer = DepositDetailSerializer(product, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# 적금 리스트 조회
@api_view(['GET'])
def saving_product_list(request):
    queryset = SavingProducts.objects.annotate(
        interest_count=Count('interest_users', distinct=True),
        joined_count=Count('joined_users', distinct=True)
    )

    # 검색 기능 추가
    search_term = request.query_params.get('search')
    if search_term:
        queryset = queryset.filter(fin_prdt_nm__icontains = search_term)

    # 필터링 처리
    intr_rate_type_nm = request.query_params.get('intr_rate_type_nm')
    kor_co_nm = request.query_params.get('kor_co_nm')
    if intr_rate_type_nm:
        queryset = queryset.filter(savingoptions__intr_rate_type_nm=intr_rate_type_nm)
    if kor_co_nm:
        queryset = queryset.filter(kor_co_nm__icontains=kor_co_nm)

    # 정렬 처리
    ordering = request.query_params.get('ordering')
    allowed_ordering = ['interest_count', '-interest_count', 'joined_count', '-joined_count']
    if ordering in allowed_ordering:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('id')  # 기본 정렬

    serializer = SavingListSerializer(
        queryset.prefetch_related('savingoptions_set'), 
        many=True, 
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['GET'])
def saving_detail(request, product_id):
    product = get_object_or_404(
        SavingProducts.objects
        .prefetch_related('savingoptions_set')
        .annotate(
            joined_count=Count('joined_users', distinct=True),
            interest_count=Count('interest_users', distinct=True)
        ),
        id=product_id
    )
    serializer = SavingDetailSerializer(product, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# 찜하기, 가입하기
# 예금 찜하기 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_interest(request, product_id):
    product = get_object_or_404(DepositProducts, id=product_id)
    interest, created = DepositInterest.objects.get_or_create(user=request.user, product=product)
    
    if created:
        # 찜하기 추가
        serializer = DepositInterestSerializer(interest)
        return Response({'action': 'added', 'data': serializer.data}, status=201)
    else:
        # 찜하기 삭제
        interest.delete()
        return Response({'action': 'removed'}, status=200)

# 적금 찜하기 토글
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saving_interest(request, product_id):
    product = get_object_or_404(SavingProducts, id=product_id)
    interest, created = SavingInterest.objects.get_or_create(user=request.user, product=product)
    
    if created:
        serializer = SavingInterestSerializer(interest)
        return Response({'action': 'added', 'data': serializer.data}, status=201)
    else:
        interest.delete()
        return Response({'action': 'removed'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_join(request, product_id):
    """
    예금 상품 가입 토글 (가입/가입 취소)
    """
    product = get_object_or_404(DepositProducts, id=product_id)
    join, created = DepositJoin.objects.get_or_create(
        user=request.user,
        product=product
    )
    if created:
        # 가입 완료
        serializer = DepositJoinSerializer(join)
        join_count = DepositJoin.objects.filter(product=product).count()
        return Response({
            'message': '가입 완료',
            'action': 'joined',
            'join_count': join_count,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        # 이미 가입되어 있으면 취소(삭제)
        join.delete()
        join_count = DepositJoin.objects.filter(product=product).count()
        return Response({
            'message': '가입 취소',
            'action': 'canceled',
            'join_count': join_count
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saving_join(request, product_id):
    """
    적금 상품 가입 토글 (가입/가입 취소)
    """
    product = get_object_or_404(SavingProducts, id=product_id)
    join, created = SavingJoin.objects.get_or_create(
        user=request.user,
        product=product
    )
    if created:
        # 가입 완료
        serializer = SavingJoinSerializer(join)
        join_count = SavingJoin.objects.filter(product=product).count()
        return Response({
            'message': '가입 완료',
            'action': 'joined',
            'join_count': join_count,
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    else:
        # 이미 가입되어 있으면 취소(삭제)
        join.delete()
        join_count = SavingJoin.objects.filter(product=product).count()
        return Response({
            'message': '가입 취소',
            'action': 'canceled',
            'join_count': join_count
        }, status=status.HTTP_200_OK)

        
# 내 목록 조회
# 찜 상품 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_interests(request):
    deposit_interests = DepositInterest.objects.filter(
        user=request.user
    ).select_related('product')
    
    saving_interests = SavingInterest.objects.filter(
        user=request.user
    ).select_related('product')
    
    deposit_serializer = DepositInterestSerializer(deposit_interests, many=True)
    saving_serializer = SavingInterestSerializer(saving_interests, many=True)
    
    return Response({
        'deposits': deposit_serializer.data,
        'savings': saving_serializer.data
    })
    
# 가입 상품 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_joins(request):
    deposit_joins = DepositJoin.objects.filter(
        user=request.user
    ).select_related('product')
    
    saving_joins = SavingJoin.objects.filter(
        user=request.user
    ).select_related('product')
    
    deposit_serializer = DepositJoinSerializer(deposit_joins, many=True)
    saving_serializer = SavingJoinSerializer(saving_joins, many=True)
    
    return Response({
        'deposits': deposit_serializer.data,
        'savings': saving_serializer.data
    })
    